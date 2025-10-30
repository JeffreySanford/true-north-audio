
import { Injectable } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { VideoAsset } from '../models/video-asset.model';
import { Subject } from 'rxjs';

@Injectable()
export class VideoAssetService {
  private createSubject = new Subject<VideoAsset>();
  private findAllSubject = new Subject<VideoAsset[]>();
  private findByIdSubject = new Subject<VideoAsset | null>();
  private updateSubject = new Subject<VideoAsset | null>();
  private deleteSubject = new Subject<VideoAsset | null>();

  constructor(@InjectModel('VideoAsset') private readonly videoAssetModel: Model<VideoAsset>) {}

  create(data: Partial<VideoAsset>) {
    this.videoAssetModel.create(data)
      .then(result => this.createSubject.next(result))
      .catch(err => this.createSubject.error(err));
    return this.createSubject.asObservable();
  }

  findAll() {
    this.videoAssetModel.find().exec()
      .then(result => this.findAllSubject.next(result))
      .catch(err => this.findAllSubject.error(err));
    return this.findAllSubject.asObservable();
  }

  findById(id: string) {
    this.videoAssetModel.findById(id).exec()
      .then(result => this.findByIdSubject.next(result))
      .catch(err => this.findByIdSubject.error(err));
    return this.findByIdSubject.asObservable();
  }

  update(id: string, data: Partial<VideoAsset>) {
    this.videoAssetModel.findByIdAndUpdate(id, data, { new: true }).exec()
      .then(result => this.updateSubject.next(result))
      .catch(err => this.updateSubject.error(err));
    return this.updateSubject.asObservable();
  }

  delete(id: string) {
    this.videoAssetModel.findByIdAndDelete(id).exec()
      .then(result => this.deleteSubject.next(result))
      .catch(err => this.deleteSubject.error(err));
    return this.deleteSubject.asObservable();
  }
}
