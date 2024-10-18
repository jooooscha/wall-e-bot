{
  lib,
  buildPythonPackage,
  fetchPypi,
  poetry-core,
  aiofiles,
  aiohttp,
  aiohttp-socks,
  h11,
  h2,
  jsonschema,
  pycryptodome,
  unpaddedbase64,
  atomicwrites,
  cachetools,
  peewee,
  python-olm,
}:

buildPythonPackage rec {
  pname = "matrix-nio";
  version = "0.24.0";
  pyproject = true;

  src = fetchPypi {
    pname = "matrix_nio";
    inherit version;
    hash = "sha256-dfnFiVjb41O+wpvhhUg1322R5vO+KVImGjonyZ6olrk=";
  };

  build-system = [
    poetry-core
  ];

  dependencies = [
    aiofiles
    aiohttp
    aiohttp-socks
    h11
    h2
    jsonschema
    pycryptodome
    unpaddedbase64
    atomicwrites
    cachetools
    peewee
    python-olm
  ];

  optional-dependencies = {
    e2e = [
      atomicwrites
      cachetools
      peewee
      python-olm
    ];
  };

  # pythonImportsCheck = [
  #   "matrix_nio"
  # ];

  meta = {
    description = "A Python Matrix client library, designed according to sans I/O principles";
    homepage = "https://pypi.org/project/matrix-nio/0.24.0/";
    license = lib.licenses.isc;
    maintainers = with lib.maintainers; [ ];
  };
}
