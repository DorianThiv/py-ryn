# SERVER PROTOTYPE - RYN SRV

This server is a prototype to manage few data with generic modules.

## Getting Started

RYN Structure:
 _________________________________________________________________________
|core  |            | module     |________________________________________|
|______|____________|____________|________________________________________|
|                   |                                                     |
|core --- loader ---|---managers --- providers --- operators --- binders  |
|            |      |      |                           |                  |
|            |      |      |                           |                  |
|          dealer---|------+                        regisrty              |
|            |      |_____________________________________________________|                                     
|            |      | specifics (commands, exceptions, classes)           |
|         directory |                                                     |
|___________________|_____________________________________________________|

* Core:
The core is compose: core, loader, dealer, directory
    * core: lauch the program with a simple lifecycle (start, run, stop)
    * loader: load all module specifies in the config.json
    * dealer: manage exanges between the modules
    * directory: store all modules in which loaded by loader 

* Modules : 
A module provide one or many differents data. A module have a name with "mdl" before and a prefix in lower case.

```
Exemple: (name: "mdlmymodule", prefix: "mymodule")
```

In a module there are components.
A component can be a "manager", a "provider", an "operator", a "registry" and a "binder".
A module must have theses five components to be functionnal.
Each components have minimum one class. 
The class name must be in Camel Case to be correctly interpreted by RYN.
It will be formated like this:

```
Exemple: MyModuleManager, MyModuleProvider, MyModuleOperator, MyModuleBinder
```

### Prerequisites

What things you need to install the software and how to install them

```
Execute : ./core.py
```

### Installing

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Python36](https://www.python.org/downloads/) - Programming language
* [GitBash](http://gitforwindows.org/) - Git console on Windows

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **THIVOLLE Dorian** - *Initial work* - [DorianThiv](https://github.com/DorianThiv)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Generics Systems
* Threading
* Servers
* SMA
* etc ...


