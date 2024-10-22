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

        callPackage = pkgs.lib.callPackageWith (pkgs // pkgs.python3Packages);
        python = pkgs.python3;

        python-cryptography-fernet-wrapper = callPackage ./deps/python-cryptography-fernet-wrapper.nix { };
        aiohttp-socks-0-8-4 = callPackage ./deps/aiohttp-socks-0-8-4.nix { };
        matrix-nio-0-24-0 = callPackage ./deps/matrix-nio-0-24-0.nix {
          aiohttp-socks = aiohttp-socks-0-8-4;
        };

        simplematrixbotlib = callPackage ./deps/simplematrixbotlib.nix {
          inherit python-cryptography-fernet-wrapper;
          matrix-nio = matrix-nio-0-24-0;
        };

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
            env.PYTHONUNBUFFERED = "1";
          });
      }
    );
}
