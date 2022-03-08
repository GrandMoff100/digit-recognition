# square-circle-ai

Implementing Rosenblatt's perceptron algorithm (zero intermediate-neuron layers) distinguishing circle vs square images in pure python. (Educational Purposes only)

## Pre-requisites

### Generating the Training and Testing Datasets

```bash
python -m dataset <size>  # Generates a rectangles and circles directory with training images for the Model
```

## Help

```bash
$ python -m model
Usage: python -m model [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  test   Uses a trained model on an image and outputs the prediction.
  train  Trains a model on the images in `<dataset-folder>/rectangle` and...
```

### Training

```bash
Usage: python -m model train [OPTIONS] SIZE BIAS

  Trains a model on the images in `<dataset-folder>/rectangle` and `<dataset-folder>/circle`
  folders.

Options:
  -d, --dataset-folder PATH
  -r, --input-weights-file FILENAME
  -w, --output-weights-file FILENAME
  --help                                Show this message and exit.
  ```

### Testing

```bash
$ python -m model test --help
Usage: python -m model test [OPTIONS] SIZE BIAS WEIGHTS_FILE [FILES]...

  Uses a trained model on an image and outputs the prediction.

Options:
  -v, --verbose  Show the guesses for the individual input files
  --help         Show this message and exit.
```
