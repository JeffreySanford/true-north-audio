
import { Injectable } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { VideoAsset } from '../models/video-asset.model';
import { ReplaySubject } from 'rxjs';

@Injectable()
export class VideoAssetService {

  constructor(@InjectModel('VideoAsset') private readonly videoAssetModel: Model<VideoAsset>) {}

  create(data: Partial<VideoAsset>) {
    this.videoAssetModel.create(data)
    const subject = new ReplaySubject(1);
    this.videoAssetModel.create(data)
      .then(result => {
        subject.next(result);
        subject.complete();
      })
      .catch(err => subject.error(err));
    return subject.asObservable();
  }

  findAll() {
    this.videoAssetModel.find().exec()
    const subject = new ReplaySubject(1);
    this.videoAssetModel.find().exec()
      .then(result => {
        subject.next(result);
        subject.complete();
      })
      .catch(err => subject.error(err));
    return subject.asObservable();
  }

  findById(id: string) {
    this.videoAssetModel.findById(id).exec()
    const subject = new ReplaySubject(1);
    this.videoAssetModel.findById(id).exec()
      .then(result => {
        subject.next(result);
        subject.complete();
      })
      .catch(err => subject.error(err));
    return subject.asObservable();
  }

  update(id: string, data: Partial<VideoAsset>) {
    this.videoAssetModel.findByIdAndUpdate(id, data, { new: true }).exec()
    const subject = new ReplaySubject(1);
    this.videoAssetModel.findByIdAndUpdate(id, data, { new: true }).exec()
      .then(result => {
        subject.next(result);
        subject.complete();
      })
      .catch(err => subject.error(err));
    return subject.asObservable();
  }

  delete(id: string) {
    this.videoAssetModel.findByIdAndDelete(id).exec()
    const subject = new ReplaySubject(1);
    this.videoAssetModel.findByIdAndDelete(id).exec()
      .then(result => {
        subject.next(result);
        subject.complete();
      })
      .catch(err => subject.error(err));
    return subject.asObservable();
  }
}
