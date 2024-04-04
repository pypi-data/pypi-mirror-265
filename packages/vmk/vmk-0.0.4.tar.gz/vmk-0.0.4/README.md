# vmk

![](https://cdn.discordapp.com/attachments/823396088605573170/831609055792463872/rsz_axggz5fpxpf2aaaaaelftksuqmcc.png?ex=661ecec9&is=660c59c9&hm=06ee2bf8150322d716347a0622f07a230e528514f82ee7dcdc70d44104b211ef&)

Simple command-line PDF combiner.

## Installation

`pip install vmk`

## Usage

Simply running `vmk` will combine all PDF files in the current directory's first pages into a single file.
You can use the options below (or running `vmk --help`) to customise the behaviour.

### Options

| Option          | Description                                     |
| --------------- | ----------------------------------------------- |
| `-f`, `--files` | Select the PDF files to combine                 |
| `-d`, `--dir`   | Select a directory whose files will be combined |
| `-o`, `--out`   | The output file name                            |
