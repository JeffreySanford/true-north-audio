import { IsString, IsOptional } from 'class-validator';

export class CreateVocalFeatureDto {
  @IsString()
  name!: string;

  @IsString()
  @IsOptional()
  description?: string;
}
