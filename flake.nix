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
          # pyyaml
          requests
          pyppeteer
          # scrapy
          selenium
          webdriver-manager
          matplotlib
          numpy
          # (
            # buildPythonPackage rec {
              # pname = "deserialize";
              # version = "1.8.3";
              # src = fetchPypi {
                # inherit pname version;
                # sha256 = "sha256-0aozmQ4Eb5zL4rtNHSFjEynfObUkYlid1PgMDVmRkwY=";
              # };
              # doCheck = false;
              # buildInputs = []; # pkgs deps
              # nativeBuildInputs = []; # pkgs deps
              # propagatedBuildInputs = []; # python deps
            # }
          # )
        ]);

      in {
        packages = { };
        apps = { };

        devShells.default =
          pkgs.mkShell {
            name = "Python Shell";
            packages = [
              packaged-python
              pkgs.nix-init
              pkgs.sqlite-web
            ];
          };
      }
    );
}
