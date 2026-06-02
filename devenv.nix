 {
  pkgs,
  lib,
  config,
  ...
}:
{
  # https://devenv.sh/packages/
  packages = [
    pkgs.openjdk17
  ];
  # https://devenv.sh/languages/
  languages = {
    python = {
      enable = true;
      package = pkgs.python313.withPackages (ps: [
        ps.pyspark
        ps.numpy
      ]);
      lsp.package = pkgs.basedpyright;
    };
  };

  # https://devenv.sh/reference/options/
  env = {
    JAVA_HOME = pkgs.openjdk17.home;
  };

  enterShell = ''
    echo "Java  [$JAVA_HOME]"
  '';

  # See full reference at https://devenv.sh/reference/options/
} 
