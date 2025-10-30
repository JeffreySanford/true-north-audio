
import { Injectable } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { VocalFeature } from '../models/vocal-feature.model';
import { Subject } from 'rxjs';

@Injectable()
export class VocalFeatureService {
  private createSubject = new Subject<VocalFeature>();
  private findAllSubject = new Subject<VocalFeature[]>();
  private findByIdSubject = new Subject<VocalFeature | null>();
  private updateSubject = new Subject<VocalFeature | null>();
  private deleteSubject = new Subject<VocalFeature | null>();

  constructor(@InjectModel('VocalFeature') private readonly vocalFeatureModel: Model<VocalFeature>) {}

  create(data: Partial<VocalFeature>) {
    this.vocalFeatureModel.create(data)
      .then(result => this.createSubject.next(result))
      .catch(err => this.createSubject.error(err));
    return this.createSubject.asObservable();
  }

  findAll() {
    this.vocalFeatureModel.find().exec()
      .then(result => this.findAllSubject.next(result))
      .catch(err => this.findAllSubject.error(err));
    return this.findAllSubject.asObservable();
  }

  findById(id: string) {
    this.vocalFeatureModel.findById(id).exec()
      .then(result => this.findByIdSubject.next(result))
      .catch(err => this.findByIdSubject.error(err));
    return this.findByIdSubject.asObservable();
  }

  update(id: string, data: Partial<VocalFeature>) {
    this.vocalFeatureModel.findByIdAndUpdate(id, data, { new: true }).exec()
      .then(result => this.updateSubject.next(result))
      .catch(err => this.updateSubject.error(err));
    return this.updateSubject.asObservable();
  }

  delete(id: string) {
    this.vocalFeatureModel.findByIdAndDelete(id).exec()
      .then(result => this.deleteSubject.next(result))
      .catch(err => this.deleteSubject.error(err));
    return this.deleteSubject.asObservable();
  }
}
