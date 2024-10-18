{
  lib,
  buildPythonPackage,
  fetchPypi,
  poetry-core,
  markdown,
  matrix-nio,
  pillow,
  python-cryptography-fernet-wrapper,
  toml,
}:

buildPythonPackage rec {
  pname = "simplematrixbotlib";
  version = "2.12.0";
  pyproject = true;

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-uNNXqdMu+FKEI1UExkuIWUP6H7hQo6t8solFX8LufrA=";
  };

  build-system = [
    poetry-core
  ];

  dependencies = [
    markdown
    matrix-nio
    pillow
    python-cryptography-fernet-wrapper
    toml
  ];

  pythonImportsCheck = [
    "simplematrixbotlib"
  ];

  meta = {
    description = "An easy to use bot library for the Matrix ecosystem written in Python";
    homepage = "https://pypi.org/project/simplematrixbotlib/";
    license = lib.licenses.mit;
    maintainers = with lib.maintainers; [ ];
  };
}
