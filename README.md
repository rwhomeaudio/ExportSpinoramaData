# ExportSpinoramaData
ExportSpinoramaData is a simple tool to export Spinorama data from [spinorama](https://github.com/pierreaubert/spinorama) (see also [SPINorma](https://www.spinorama.org/)) as CSV text textfiles. It uses the loudspeaker measurement database and APIs from [spinorama](https://github.com/pierreaubert/spinorama) and is written in [Python 3](https://www.python.org/). The [actual measurement data of spinorama](https://github.com/pierreaubert/spinorama/tree/develop/datas/measurements) comes from various providers (see [spinorama.org](https://www.spinorama.org/docs/06_sources.html)).

The expoted data (CEA2034, Early Refections and Estimated In-Room Response) can directly be imported into various tools, e.g. [REW](https://www.roomeqwizard.com/), [FreqRespGraph](https://github.com/rwhomeaudio/FreqRespGraph) or spreadsheet software for display and further processing.

# Installation

# Usage
```
ExportSpinoramaData.py -h
usage: ExportSpinoramaData [-h] [--absSPL] speaker version

ExportSpinoramaData exports spinorama data of a given speaker model and measurement version as text files in a sub directory "export".
The exported files can e.g. directly be imported in REW or spreadsheet programs.

positional arguments:
  speaker
  version

options:
  -h, --help  show this help message and exit
  --absSPL    Export data with absolute SPL instead of 0dB normalized, default off

Example:

  ExportSpinoramaData.py --absSPL "KEF LS50 Meta" "asr"

  creates

    export/KEF LS50 Meta/asr/CEA2034/All.csv
    export/KEF LS50 Meta/asr/CEA2034/Early Reflections DI.txt
    export/KEF LS50 Meta/asr/CEA2034/On Axis.txt
    export/KEF LS50 Meta/asr/CEA2034/Early Reflections.txt
    export/KEF LS50 Meta/asr/CEA2034/Sound Power.txt
    export/KEF LS50 Meta/asr/CEA2034/DI offset.txt
    export/KEF LS50 Meta/asr/CEA2034/Listening Window.txt
    export/KEF LS50 Meta/asr/CEA2034/Sound Power DI.txt
    export/KEF LS50 Meta/asr/Estimated In-Room Response.txt
    export/KEF LS50 Meta/asr/Early Reflections/Front Wall Bounce.txt
    export/KEF LS50 Meta/asr/Early Reflections/All.csv
    export/KEF LS50 Meta/asr/Early Reflections/Total Early Reflection.txt
    export/KEF LS50 Meta/asr/Early Reflections/Floor Bounce.txt
    export/KEF LS50 Meta/asr/Early Reflections/Rear Wall Bounce.txt
    export/KEF LS50 Meta/asr/Early Reflections/Ceiling Bounce.txt
    export/KEF LS50 Meta/asr/Early Reflections/Side Wall Bounce.txt

  from the measurement of the KEF LS50 Meta provided by Audio Science Review with absolute SPL.
  
  Use

  ExportSpinoramaData.py --absSPL '*' '*'

  to export all availabile measurements.

```
# Examples
