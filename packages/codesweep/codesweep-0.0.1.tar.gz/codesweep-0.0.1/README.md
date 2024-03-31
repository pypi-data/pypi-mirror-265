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


## Roadmap
Our vision for CodeSweep is to continually enhance its capabilities and ease of use. Here's what's on the horizon:
1. **Complete Testing:** Implement comprehensive testing across the tool to ensure reliability and stability.
2. **User Configuration:** Introduce the ability for users to customize and configure CodeSweep to fit their specific needs. This includes making it easier for users to work with configuration files by implementing a unified configuration format that simplifies setup and customization.
3. **Automatically Generate GitHub CI Actions:** Develop functionality to automatically generate GitHub CI actions based on CodeSweep's configuration, making continuous integration seamless and more efficient.

## Contributing
Contributions are welcome! If you have suggestions for improvements or want to contribute to the roadmap, please feel free to open an issue or submit a pull request.

## License
CodeSweep is released under the MIT License. See the [LICENSE](LICENSE) file for more details.
