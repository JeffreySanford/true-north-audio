
import { Injectable } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { VocalFeature } from '../models/vocal-feature.model';
import { ReplaySubject } from 'rxjs';

@Injectable()
export class VocalFeatureService {

  constructor(@InjectModel('VocalFeature') private readonly vocalFeatureModel: Model<VocalFeature>) {}

  create(data: Partial<VocalFeature>) {
    this.vocalFeatureModel.create(data)
      const subject = new ReplaySubject(1);
      this.vocalFeatureModel.create(data)
        .then(result => {
          subject.next(result);
          subject.complete();
        })
        .catch(err => subject.error(err));
      return subject.asObservable();
  }

  findAll() {
    this.vocalFeatureModel.find().exec()
      const subject = new ReplaySubject(1);
      this.vocalFeatureModel.find().exec()
        .then(result => {
          subject.next(result);
          subject.complete();
        })
        .catch(err => subject.error(err));
      return subject.asObservable();
  }

  findById(id: string) {
    this.vocalFeatureModel.findById(id).exec()
      const subject = new ReplaySubject(1);
      this.vocalFeatureModel.findById(id).exec()
        .then(result => {
          subject.next(result);
          subject.complete();
        })
        .catch(err => subject.error(err));
      return subject.asObservable();
  }

  update(id: string, data: Partial<VocalFeature>) {
    this.vocalFeatureModel.findByIdAndUpdate(id, data, { new: true }).exec()
      const subject = new ReplaySubject(1);
      this.vocalFeatureModel.findByIdAndUpdate(id, data, { new: true }).exec()
        .then(result => {
          subject.next(result);
          subject.complete();
        })
        .catch(err => subject.error(err));
      return subject.asObservable();
  }

  delete(id: string) {
    this.vocalFeatureModel.findByIdAndDelete(id).exec()
      const subject = new ReplaySubject(1);
      this.vocalFeatureModel.findByIdAndDelete(id).exec()
        .then(result => {
          subject.next(result);
          subject.complete();
        })
        .catch(err => subject.error(err));
      return subject.asObservable();
  }
}
