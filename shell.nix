let
  pkgs = import <nixpkgs> {};
in
  pkgs.mkShell {
    packages = [
      pkgs.win2xcur
      pkgs.xcur2png
      pkgs.xcursorgen
      pkgs.imagemagick
    ];

    shellHook = ''
      ${pkgs.zsh}/bin/zsh
    '';
  }
