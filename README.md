# Post-Quantum Cryptography: LWE Encrypted Messaging

This is my final-year project for my BSc Mathematics and Computer Science degree at the University of Birmingham.

The project looks at **post-quantum cryptography**, focusing specifically on **Learning with Errors (LWE)** and Regev's encryption scheme. I implemented the encryption scheme from scratch and then used it to build a simple end-to-end encrypted messaging system using Python and TCP sockets.

The main aim of the project was to understand the mathematics behind LWE and then see what happens when that mathematical construction is turned into a working piece of software.

> **Note:** This is an academic project and is not intended to be used as a production cryptographic system. There are several known security limitations, which are discussed below and in the full report.

## What does it do?

The final implementation allows two clients to communicate through a relay server.

When a client starts, it generates an LWE key pair and exchanges its public key with the other client through the server. Messages are converted into bits and encrypted before being sent across the network. The receiving client then decrypts the ciphertext and reconstructs the original message.

The server only acts as a relay and does not have access to the plaintext messages.

At a high level, the process looks like this:

```text
Client A
   │
   │  Public key
   ▼
Relay Server
   │
   │  Public key
   ▼
Client B

Client A
   │
   │  Encrypted message
   ▼
Relay Server
   │
   │  Encrypted message
   ▼
Client B
   │
   ▼
 Decryption
   │
   ▼
Plaintext
```

## Why LWE?

Current public-key cryptography relies heavily on mathematical problems such as integer factorisation and discrete logarithms. These problems are vulnerable to Shor's algorithm, which could potentially make widely used systems such as RSA and elliptic-curve cryptography insecure if sufficiently powerful quantum computers become available.

This led me to investigate **post-quantum cryptography**, and more specifically lattice-based cryptography.

I chose LWE because it has a strong mathematical foundation and gave me an opportunity to combine both the Mathematics and Computer Science sides of my degree.

The scheme I implemented is **Regev's encryption scheme**, which is one of the foundational LWE constructions behind later lattice-based cryptographic schemes.

## Regev's LWE encryption scheme

The implementation follows the basic structure of Regev's scheme.

### Key generation

A secret vector is generated:

```text
s ∈ Zq^n
```

The public key is then constructed from a collection of LWE samples:

```text
b = <a, s> + e (mod q)
```

where `a` is a random vector and `e` is a small error term.

### Encryption

To encrypt a bit, a random binary selection of the public-key samples is made. The selected samples are combined to produce the ciphertext.

The plaintext bit is represented by adding either `0` or approximately `q/2`.

### Decryption

The recipient uses their secret key to calculate the difference between the two ciphertext components.

If the accumulated error remains small enough, the result will be close to either:

```text
0
```

or

```text
q / 2
```

allowing the original bit to be recovered.

The complete mathematical explanation is included in the project report.

## Implementation

I developed the project in several stages rather than writing the complete messaging system immediately.

### `key_generation`

This contains the initial development of the key generation, encryption and decryption algorithms.

Development eventually led to:

```text
PKgen6.py
```

which was the fully working and verified version of the initial implementation.

There is also a `test.py` file which I used while experimenting with NumPy arrays and testing parts of the implementation.

### `encryption_scheme`

The next stage separated the cryptographic operations into different files to make the code more modular.

The `main.py` file brings the components together and allows a bit-string to be encrypted and then decrypted.

### `network_code`

This was the first stage where the encryption scheme was integrated with networking.

A relay server and multiple clients were introduced here. This was an intermediate development stage, and the encryption was not yet working correctly.

### `pre-release`

This contains the more complete messaging system before the final cleanup.

There are several versions of the client and server in this directory. These are useful for showing how the implementation changed during development.

For example:

```text
Client B/
    client.py
    client2.py

server/
    server.py
    server2.py
    server3.py
```

The later versions contain the main changes and improvements made during development.

### `final_release`

This is the final version of the project.

Unused files from development have been removed and the code has been cleaned up and refined.

This directory contains the implementation presented as part of the final project.

## Networking

The messaging system uses TCP sockets to allow two clients to communicate through a relay server.

The server is responsible for forwarding information between the clients and handling the exchange of public keys.

The clients perform the actual encryption and decryption, meaning that the server does not have access to the plaintext.

Because TCP is a stream-based protocol, I also implemented a simple framing system. Each message is prefixed with a 4-byte big-endian integer containing the length of the following payload.

## Parameters

The implementation uses the following parameters:

| Parameter |                      Value |
| --------- | -------------------------: |
| `n`       |                        256 |
| `q`       |                      32768 |
| `m`       | `(1 + 0.1)(n + 1) log₂(q)` |
| `σ`       |                        2.8 |

These parameters were chosen to allow the scheme to be demonstrated and tested effectively.

They are **not production cryptographic parameters**. The project was primarily concerned with understanding the scheme and demonstrating that it could be implemented correctly.

## Results

The final implementation was able to encrypt and decrypt messages successfully between two clients.

One of the main things I found during the project was how inefficient the original Regev scheme is compared with more modern lattice-based schemes.

The implementation encrypts one bit at a time, meaning that even short messages result in relatively large ciphertexts.

This was a useful demonstration of the difference between understanding the mathematical construction of a cryptographic scheme and designing something that is practical to deploy.

## Security limitations

There are several important limitations to this implementation.

### Parameters

The parameters used are too small to provide production-level security. In particular, the underlying LWE instances may be vulnerable to lattice-reduction attacks.

### Authentication

The key exchange is not authenticated. This means the system is vulnerable to a man-in-the-middle attack because an attacker could potentially replace a client's public key during the exchange.

### `pickle`

The networking implementation uses Python's `pickle` module to serialise ciphertext.

This is not appropriate for handling untrusted data in a production security-sensitive application because malicious pickle data can result in arbitrary code execution.

### Error distribution

The implementation uses the Box-Muller transformation to generate Gaussian error values before rounding them to integers.

This was sufficient for the purposes of the project, but the approach has limitations compared with the requirements of a production cryptographic implementation.

Because of these issues, this project should be viewed as an **implementation and learning exercise rather than a secure messaging application**.

## What I learned

This project gave me the opportunity to work across several areas that I am interested in:

* Post-quantum cryptography
* Lattice-based cryptography
* Learning with Errors
* Mathematical cryptography
* Python
* NumPy
* TCP networking
* Client/server systems
* Binary data and serialisation
* Security analysis

The most useful part of the project was implementing the mathematical definition of Regev's scheme myself and then seeing how it behaved when integrated into a real networked application.

## Repository structure

```text
.
├── key_generation/
├── encryption_scheme/
├── network_code/
├── pre-release/
├── final_release/
├── docs/
│   └── final-year-project-report.pdf
└── README.md
```

The earlier directories are included to show the development process. The **`final_release`** directory contains the finished implementation.

## Full report

The full project report is available here:

**[Final Year Project Report](docs/final-year-project-report.pdf)**

The report contains the full mathematical background, explanation of LWE and Regev's scheme, implementation details, parameter selection, testing, security analysis and conclusions.

## Disclaimer

This project was created for academic purposes and should not be used to protect real-world sensitive information.

It demonstrates the concepts behind LWE-based encryption, but the implementation has known limitations and has not been designed or audited for production use.

---

**Harry Day**
BSc Mathematics and Computer Science
University of Birmingham
