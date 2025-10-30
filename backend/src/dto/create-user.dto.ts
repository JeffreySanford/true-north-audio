import { IsString, IsArray, IsOptional } from 'class-validator';

export class CreateUserDto {
  @IsString()
  username!: string;

  @IsArray()
  @IsOptional()
  roles?: string[];
}
