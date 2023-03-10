# Inference Engine (Designed for Geometry Theorem Proving)

## Structure

Geometry objects has properties that databases normally dont have, such as symmetry in terms of points construction
and transitivity. As a result, we implement an inference engine that are designed for geometry theorem proving.
The structure of geometry objects are as follows

`primitives.py`

- Point
- LineKey
- Angle
- Segment
- Ratio
- Triangle
- CongKey

`database.py`

- lines: dict[LineKey, set[Point]]
- congs: dict[CongKey, set[Segment]]
- midpFacts: list[list[Point]]
- paraFacts: list[set[LineKey]]
- perpFacts: list[set[LineKey]]
- eqangleFacts: list[set[Angle]]
- eqratioFacts: list[set[Ratio]]
- simtriFacts: list[set[Triangle]]
- contriFacts: list[set[Triangle]]