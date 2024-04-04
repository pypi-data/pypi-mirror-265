
from typing import Optional
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import ed25519
from .utils import keccak_256
from .certificate_management import create_csr
from .registry import Registry


class AutoEntity:
    name: str
    private_key: Optional[ed25519.Ed25519PrivateKey]
    registry: Optional[Registry]
    certificate: Optional[x509.Certificate]

    def __init__(self, name: str, private_key=None, registry: Optional[Registry] = None):
        self.name = name
        self.registry = registry
        self.id = keccak_256(name.encode())
        self.private_key = private_key
        self.certificate = None

    def load_certificate_from_registry(self):
        """
        Load the certificate of the entity from the registry.

        :return: Certificate of the entity.
        """

        if self.registry is None:
            return None

        certificate = self.registry.get_certificate(self.name)
        self.certificate = certificate

        # TODO: Verify certificate matches the public key of the entity

        return certificate

    def create_csr(self):
        """
        Creates a Certificate Signing Request (CSR).

        :param private_key: Private key to sign the CSR with.
        :return: Created X.509 CertificateSigningRequest.
        """

        if self.private_key is None:
            return None

        csr = create_csr(self.name, self.private_key)

        return csr
