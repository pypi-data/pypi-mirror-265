# CodeSweep: Simplify Your Code Maintenance


**Documentation**: <a href="https://joehaddad2000.github.io/codesweep/" target="_blank">https://joehaddad2000.github.io/codesweep/</a>

**Source Code**: <a href="https://github.com/joehaddad2000/codesweep" target="_blank">https://github.com/joehaddad2000/codesweep</a>

---

CodeSweep is a streamlined CLI tool designed to simplify the process of maintaining a clean and type-safe codebase. It serves as an intuitive wrapper around popular libraries, providing a user-friendly interface for both beginners and those looking to avoid the complexity of direct library configuration. 

With CodeSweep, users can effortlessly perform linting, formatting and type checking, leveraging the robust capabilities of underlying tools without the need for extensive setup. Ideal for developers seeking a straightforward solution to code maintenance, CodeSweep offers an out-of-the-box approach to ensuring code quality.

## Features
- **Easy Linting and Type Checking:** Quickly lint and type check your code with minimal setup.
- **User-Friendly CLI:** A simple and intuitive command-line interface that makes code maintenance a breeze.
- **Out-of-the-Box Configuration:** Avoid the hassle of configuring multiple libraries by leveraging CodeSweep's default settings.

## Dependencies

CodeSweep leverages several outstanding open-source tools to provide its functionality. We extend our deepest gratitude to the developers and contributors of these projects:

- **[Ruff](https://docs.astral.sh/ruff/)**: For the lightning-fast linting and formatting capabilities. Its performance and ease of integration are unparalleled, making it an essential component of our tool.

- **[Mypy](https://mypy.readthedocs.io/en/stable/)**: For the robust static type checking. Mypy's ability to catch subtle type inconsistencies before runtime has been invaluable in ensuring the reliability and type safety of countless codebases.

We encourage our users to explore these tools and consider supporting their ongoing development.

## Installation
To install CodeSweep, run the following command:
```
pip install codesweep
```

## Usage
To perform a full sweep of your codebase, simply run:
```
cs sweep
```

For more detailed commands and options, use:
```
cs --help
```

## Contributing
Contributions are welcome! If you have suggestions for improvements or want to contribute to the roadmap, please feel free to open an issue or submit a pull request.

## License
CodeSweep is released under the MIT License. See the [LICENSE](LICENSE) file for more details.
