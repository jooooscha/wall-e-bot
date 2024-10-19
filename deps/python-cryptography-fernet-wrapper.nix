{
  lib,
  buildPythonPackage,
  fetchPypi,
  setuptools,
  wheel,
  cryptography,
}:

buildPythonPackage rec {
  pname = "python-cryptography-fernet-wrapper";
  version = "1.0.4";
  pyproject = true;

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-dPEYr612POscHqq6awbhnMNeXP+0AI5xVGdRcfoRapI=";
  };

  build-system = [
    setuptools
    wheel
  ];

  dependencies = [
    cryptography
  ];

  # pythonImportsCheck = [
  #   "python_cryptography_fernet_wrapper"
  # ];

  meta = {
    description = "A wrapper for cryptography.fernet";
    homepage = "https://pypi.org/project/python-cryptography-fernet-wrapper/";
    license = lib.licenses.gpl3Only;
    maintainers = with lib.maintainers; [ ];
  };
}
