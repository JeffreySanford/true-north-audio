import { IsString } from 'class-validator';

export class CreateVideoAssetDto {
  @IsString()
  title!: string;

  @IsString()
  filePath!: string;
}
