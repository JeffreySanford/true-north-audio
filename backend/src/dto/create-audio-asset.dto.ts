import { IsString, IsArray, IsOptional } from 'class-validator';

export class CreateAudioAssetDto {
  @IsString()
  title!: string;

  @IsString()
  genre!: string;

  @IsArray()
  @IsOptional()
  vocalFeatures?: string[];

  @IsString()
  filePath!: string;
}
