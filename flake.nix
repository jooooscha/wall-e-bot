{
  description = "A basic flake using pyproject.toml project metadata";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    pyproject-nix = {
      url = "github:nix-community/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { nixpkgs, pyproject-nix, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let

        project = pyproject-nix.lib.project.loadPyproject {
          projectRoot = ./.;
        };

        pkgs = import nixpkgs {
          system = system;
          config.permittedInsecurePackages = [
            "olm-3.2.16"
          ];
          overlays = [
            # overriding python3 to include simplematrixbotlib
            (final: prev: {
               python3 = prev.python3.override {
                 packageOverrides = pyfinal: pyprev: {
                   simplematrixbotlib = simplematrixbotlib;
                 };
               };
            })
          ];
        };

        python-cryptography-fernet-wrapper = pkgs.callPackage ./deps/python-cryptography-fernet-wrapper.nix {
          inherit (pkgs.python3Packages)
            cryptography
            setuptools
            wheel
            buildPythonPackage;
        };

        aiohttp-socks-0-8-4 = pkgs.callPackage ./deps/aiohttp-socks-0-8-4.nix {
          inherit (pkgs.python3Packages)
            buildPythonPackage
            wheel
            setuptools
            python-socks
            aiohttp;
        };

        matrix-nio-0-24-0 = pkgs.callPackage ./deps/matrix-nio-0-24-0.nix {
          aiohttp-socks = aiohttp-socks-0-8-4;
          inherit (pkgs.python3Packages)
            aiofiles
            atomicwrites
            buildPythonPackage
            cachetools
            h11
            h2
            jsonschema
            peewee
            poetry-core
            pycryptodome
            python-olm
            unpaddedbase64
            aiohttp;
        };

        simplematrixbotlib = pkgs.callPackage ./deps/simplematrixbotlib.nix {
          inherit python-cryptography-fernet-wrapper;
          matrix-nio = matrix-nio-0-24-0;
          inherit (pkgs.python3Packages)
            markdown
            pillow
            poetry-core
            toml
            buildPythonPackage;
        };

        python = pkgs.python3;

      in
      {
        # Create a development shell containing dependencies from `pyproject.toml`
        devShells.default =
          let
            # Returns a function that can be passed to `python.withPackages`
            arg = project.renderers.withPackages { inherit python; };

            # Returns a wrapped environment (virtualenv like) with all our packages
            pythonEnv = python.withPackages arg;

          in
          # Create a devShell like normal.
          pkgs.mkShell {
            packages = [ pythonEnv ];
          };

        # Build our package using `buildPythonPackage
        packages.default =
          let
            # Returns an attribute set that can be passed to `buildPythonPackage`.
            attrs = project.renderers.buildPythonPackage { inherit python; };
          in
          # Pass attributes to buildPythonPackage.
            # Here is a good spot to add on any missing or custom attributes.
          python.pkgs.buildPythonPackage (attrs // {
            env.CUSTOM_ENVVAR = "hello";
          });
      }
    );
}
