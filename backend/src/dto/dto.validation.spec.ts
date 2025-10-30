import { validate } from 'class-validator';
import { CreateAudioAssetDto } from './create-audio-asset.dto';
import { CreateVideoAssetDto } from './create-video-asset.dto';
import { CreateGenreDto } from './create-genre.dto';
import { CreateVocalFeatureDto } from './create-vocal-feature.dto';
import { CreateUserDto } from './create-user.dto';

describe('DTO Validation', () => {
  describe('CreateAudioAssetDto', () => {
    it('should fail if required fields are missing', async () => {
      const dto = new CreateAudioAssetDto();
      const errors = await validate(dto);
      expect(errors.length).toBeGreaterThan(0);
    });
    it('should pass with valid data', async () => {
      const dto = new CreateAudioAssetDto();
      dto.title = 'Test';
      dto.genre = 'Pop';
      dto.filePath = '/audio/test.mp3';
      dto.vocalFeatures = ['Falsetto'];
      const errors = await validate(dto);
      expect(errors.length).toBe(0);
    });
  });

  describe('CreateVideoAssetDto', () => {
    it('should fail if required fields are missing', async () => {
      const dto = new CreateVideoAssetDto();
      const errors = await validate(dto);
      expect(errors.length).toBeGreaterThan(0);
    });
    it('should pass with valid data', async () => {
      const dto = new CreateVideoAssetDto();
      dto.title = 'Test Video';
      dto.filePath = '/video/test.mp4';
      const errors = await validate(dto);
      expect(errors.length).toBe(0);
    });
  });

  describe('CreateGenreDto', () => {
    it('should fail if required fields are missing', async () => {
      const dto = new CreateGenreDto();
      const errors = await validate(dto);
      expect(errors.length).toBeGreaterThan(0);
    });
    it('should pass with valid data', async () => {
      const dto = new CreateGenreDto();
      dto.name = 'Rock';
      dto.description = 'A genre of popular music.';
      const errors = await validate(dto);
      expect(errors.length).toBe(0);
    });
  });

  describe('CreateVocalFeatureDto', () => {
    it('should fail if required fields are missing', async () => {
      const dto = new CreateVocalFeatureDto();
      const errors = await validate(dto);
      expect(errors.length).toBeGreaterThan(0);
    });
    it('should pass with valid data', async () => {
      const dto = new CreateVocalFeatureDto();
      dto.name = 'Vibrato';
      dto.description = 'A rapid, slight variation in pitch.';
      const errors = await validate(dto);
      expect(errors.length).toBe(0);
    });
  });

  describe('CreateUserDto', () => {
    it('should fail if required fields are missing', async () => {
      const dto = new CreateUserDto();
      const errors = await validate(dto);
      expect(errors.length).toBeGreaterThan(0);
    });
    it('should pass with valid data', async () => {
      const dto = new CreateUserDto();
      dto.username = 'user1';
      dto.roles = ['admin', 'user'];
      const errors = await validate(dto);
      expect(errors.length).toBe(0);
    });
  });
});
