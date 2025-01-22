let
  pkgs = import <nixpkgs> { };
in
pkgs.mkShell {
  packages = with pkgs; [
    (python3.withPackages (
      p: with p; [
        amaranth
        amaranth-boards
        amaranth-soc
        python-lsp-server
      ]
    ))
    openfpgaloader
    trellis
    yosys
    nextpnr
    gtkwave
    icestorm
  ];

  shellHook = ''
    exec fish
  '';
}
