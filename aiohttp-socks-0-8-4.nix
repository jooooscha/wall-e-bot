{
  lib,
  buildPythonPackage,
  fetchPypi,
  setuptools,
  wheel,
  aiohttp,
  python-socks,
}:

buildPythonPackage rec {
  pname = "aiohttp-socks";
  version = "0.8.4";
  pyproject = true;

  src = fetchPypi {
    pname = "aiohttp_socks";
    inherit version;
    hash = "sha256-a2EdTOg46c8sL+1eDbpEfMhIJKbLqV3FdHYGIB2kbLQ=";
  };

  build-system = [
    setuptools
    wheel
  ];

  dependencies = [
    aiohttp
    python-socks
  ];

  pythonImportsCheck = [
    "aiohttp_socks"
  ];

  meta = {
    description = "Proxy connector for aiohttp";
    homepage = "https://pypi.org/project/aiohttp-socks/0.8.4/";
    license = lib.licenses.asl20;
    maintainers = with lib.maintainers; [ ];
  };
}
