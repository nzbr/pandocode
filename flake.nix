{

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    pnpm2nix = {
      url = "github:nzbr/pnpm2nix-nzbr";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.flake-utils.follows = "flake-utils";
    };
  };

  outputs = { self, nixpkgs, flake-utils, pnpm2nix, ... }: flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs {
        inherit system;
      };
      python = pkgs.python3.withPackages (pypi: with pypi; [
        panflute
        pylint
      ]);
    in
    {
      packages = rec {
        pandocode = pkgs.stdenv.mkDerivation rec {
          name = "pandocode";
          src = ./.;
          buildInputs = [ python pkgs.zip pkgs.which ];
          buildPhase = ''
            make -j$NIX_BUILD_CORES PY=${python}/bin/python3
          '';
          installPhase = ''
            mkdir -p $out/bin
            install -m755 pandocode.pyz $out/bin/pandocode
          '';
        };
        pandocode-live-frontend = pnpm2nix.packages.${system}.mkPnpmPackage {
          src = ./live/www;
          extraBuildInputs = [ pkgs.vips ];
          installInPlace = true;
        };
        pandocode-live = pkgs.dockerTools.buildLayeredImage {
          name = "pandocode-live";
          tag = "latest";

          contents = [
            pkgs.lighttpd
            pkgs.pandoc
            pkgs.poppler_utils
            (pkgs.texlive.combine {
                inherit (pkgs.texlive) scheme-basic algorithmicx xcolor standalone preview;
            })
            (pkgs.writeShellScriptBin "python-wrapper" ''
              export PYTHONPATH=${pkgs.runCommand "pandocode-module" {} ''
                mkdir -p $out
                cp -r ${./.}/. $out/pandocode
              ''}
              exec ${pkgs.python3.withPackages (pypi: with pypi; [
                panflute
                pdf2image
                pillow
                numpy
              ])}/bin/python3 "$@"
            '')
            (pkgs.runCommand "content" { } ''
              mkdir -p $out/var/www
              cp -vr ${pandocode-live-frontend}/. $out/var/www/
              cp -vr ${./live/cgi-bin}/. $out/var/www/cgi-bin
              cp -vr ${./live/etc}/. $out/etc
            '')
          ];

          enableFakechroot = true;
          fakeRootCommands = ''
            mkdir -p /root /etc /tmp
            echo 'root:x:0:0::/root:/noshell' > /etc/passwd
          '';

          config = {
            Cmd = [ "/bin/lighttpd" "-D" "-f" "/etc/lighttpd.conf" ];
            Env = [ "" ];
            ExposedPorts = {
              "8080/tcp" = { };
            };
          };

        };
      };
    }
  );

}
