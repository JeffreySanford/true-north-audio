import { Test, TestingModule } from '@nestjs/testing';
import { MusicGenController } from './musicgen.controller';
import { MusicGenService } from './musicgen.service';
import { HttpModule } from '@nestjs/axios';
import { of } from 'rxjs';


/**
 * Unit tests for MusicGenController.
 * Verifies endpoint wiring and service integration.
 */
describe('MusicGenController', () => {
  let controller: MusicGenController;
  let service: MusicGenService;

  /**
   * Setup test module with mocked MusicGenService and HttpModule.
   */
  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      imports: [HttpModule],
      controllers: [MusicGenController],
      providers: [
        {
          provide: MusicGenService,
          useValue: {
            generateMusic: jest.fn().mockReturnValue(of({ waveform: 'abc123', sample_rate: 22050 })),
          },
        },
      ],
    }).compile();

    controller = module.get<MusicGenController>(MusicGenController);
    service = module.get<MusicGenService>(MusicGenService);
  });

  /**
   * Should instantiate the controller.
   */
  it('should be defined', () => {
    expect(controller).toBeDefined();
  });

  /**
   * Should call service and return music data.
   */
  it('should call service and return music', (done) => {
    const dto = { genre: 'ambient', duration: 5 };
    controller.generate(dto).subscribe((result) => {
      expect(service.generateMusic).toHaveBeenCalledWith('ambient', 5, undefined, undefined, undefined, undefined, undefined, undefined);
      expect(result.waveform).toBe('abc123');
      expect(result.sample_rate).toBe(22050);
      done();
    });
  });
});
