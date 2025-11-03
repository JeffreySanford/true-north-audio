export class GenreDto {
  readonly name!: string;
  readonly description!: string;
  readonly bpm!: number;
  readonly timeSignature!: string;
  readonly groove!: string;
  readonly instruments!: string[];
  readonly mandatoryInstruments!: string[];
  readonly scriptTemplate!: string;
}

export class ToggleInstrumentDto {
  readonly genreName!: string;
  readonly instrument!: string;
  readonly enabled!: boolean;
}
