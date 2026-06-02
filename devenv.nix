{
  pkgs,
  lib,
  config,
  ...
}:
{
  # https://devenv.sh/packages/
  packages = [
    pkgs.spark3
    pkgs.openjdk17
  ];

  # https://devenv.sh/languages/
  languages = {
    python = {
      enable = true;
      package = pkgs.python3.withPackages (ps: [
        ps.pyspark
        ps.numpy
      ]);
      lsp.package = pkgs.basedpyright;
    };
  };

  # https://devenv.sh/reference/options/
  env = {
    JAVA_HOME = pkgs.openjdk17.home;
    SPARK_HOME = pkgs.spark3;
  };

  enterShell = ''
    echo "Spark [$SPARK_HOME]"
    echo "Java  [$JAVA_HOME]"
  '';

  # See full reference at https://devenv.sh/reference/options/
}
