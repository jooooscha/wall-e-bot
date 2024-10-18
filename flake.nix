{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";

    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let

        pkgs = import nixpkgs { inherit system; };

        python-cryptography-fernet-wrapper = pkgs.callPackage ./python-cryptography-fernet-wrapper.nix {
            inherit (pkgs.python3Packages)
              cryptography
              setuptools
              wheel
              buildPythonPackage;
        };

        aiohttp-socks-0-8-4 = pkgs.callPackage ./aiohttp-socks-0-8-4.nix {
          inherit (pkgs.python3Packages)
            buildPythonPackage
            wheel
            setuptools
            python-socks
            aiohttp;
        };

        matrix-nio-0-24-0 = pkgs.callPackage ./matrix-nio-0-24-0.nix {
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

        packaged-python = pkgs.python3.withPackages (p: with p; [
          # Examples
          # pyyaml
          # python-cryptography-fernet-wrapper
          (pkgs.callPackage ./simplematrixbotlib.nix {
            inherit python-cryptography-fernet-wrapper;
            matrix-nio = matrix-nio-0-24-0;
            inherit (pkgs.python3Packages)
              markdown
              pillow
              poetry-core
              toml
              buildPythonPackage;
          })
          selenium
        ]);

      in {
        packages = {
          # default = pkgs.runCommand "main" { FILE = ./main.py; } ''
          #   ${packaged-python}/bin/python $FILE
          # '';
        };
        apps = { };

        devShells.default =
          pkgs.mkShell {
            name = "Python Shell";
            LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib/";
            packages = [
              packaged-python
              # pkgs.nix-init
              # pkgs.sqlite-web
              pkgs.python3Packages.pip
            ];
          };
      }
    );
}
