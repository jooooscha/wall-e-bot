{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";

    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let

        pkgs = import nixpkgs { inherit system; };

        packaged-python = pkgs.python3.withPackages (p: with p; [
          # Examples
          # requests
          # selenium
          # webdriver-manager
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
