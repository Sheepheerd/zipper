{
  description = "Wayland automation development environment (fully Nix-managed)";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs =
    { nixpkgs, self, ... }:
    let
      inherit (nixpkgs) lib;
      forAllSystems = lib.genAttrs lib.systems.flakeExposed;
    in
    {
      packages = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          python = pkgs.python312;
        in
        {
          # ----------------------------
          # wl-find-cursor (C / Wayland)
          # ----------------------------
          wl-find-cursor = pkgs.stdenv.mkDerivation {
            pname = "wl-find-cursor";
            version = "unstable-2023-10-01";

            src = pkgs.fetchFromGitHub {
              owner = "cjacker";
              repo = "wl-find-cursor";
              rev = "44b1317141c8cc64e9da3bde56402008aca8f372";
              hash = "sha256-hCnydOVK1hKjEO9KzXAS8pjHY6Myrh3wqZ9khrkDJkA=";
            };

            nativeBuildInputs = [
              pkgs.wayland
            ];

            buildInputs = [
              pkgs.wayland-protocols
              pkgs.wayland
              pkgs.wayland-utils
              pkgs.wayland-scanner
              pkgs.wayland-protocols
            ];

            postPatch = ''
              substituteInPlace Makefile \
                --replace /usr/share/wayland-protocols \
                          ${pkgs.wayland-protocols}/share/wayland-protocols
            '';

            installPhase = ''
              mkdir -p $out/bin
              install -m0755 wl-find-cursor $out/bin/
            '';
          };

          # --------------------------------
          # wayland-automation (Python lib)
          # --------------------------------
          wayland-automation = python.pkgs.buildPythonPackage {
            pname = "wayland-automation";
            version = "2.0.6";

            src = pkgs.fetchFromGitHub {
              owner = "OTAKUWeBer";
              repo = "Wayland-automation";
              rev = "66763d7902ed770c0d9cdaacfc35911aacacea19";
              hash = "sha256-hZXyybAJE4lYMF5zccLKk6a4PWlS6yKomjyV0Y4VWu8=";
            };

            pyproject = true;

            nativeBuildInputs = with python.pkgs; [
              setuptools
              wheel
            ];

            propagatedBuildInputs = with python.pkgs; [
              evdev
            ];

            doCheck = false;
          };
        }
      );

      # ----------------------------
      # Development shell
      # ----------------------------
      devShells = forAllSystems (
        system:
        let
          pkgs = import nixpkgs {
            inherit system;
            overlays = [
              (final: prev: {
                opencv4 = prev.opencv4.override {
                  # enableGtk3 = true;
                  # enablePython = true;
                  enableGtk3 = false;
                  enablePython = false;
                };
              })
            ];
          };

          python = pkgs.python312.withPackages (ps: [
            ps.numpy
            ps.pillow
            ps.evdev
            ps.requests
            ps.opencv4
            self.packages.${system}.wayland-automation
          ]);
        in
        {
          default = pkgs.mkShell {
            packages = [
              python
              pkgs.wayland-utils
              pkgs.wtype
              self.packages.${system}.wl-find-cursor
              pkgs.feh
              pkgs.slurp
              pkgs.gimp
              pkgs.pkg-config
              pkgs.stdenv.cc.cc.lib
            ];
            shellHook = ''
              export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH
              echo "Python environment ready with OpenCV $(python -c 'import cv2; print(cv2.__version__)')"
            '';
          };
        }
      );
    };
}
