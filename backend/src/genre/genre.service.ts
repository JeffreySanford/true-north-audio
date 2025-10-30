
import { Injectable } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { Genre } from '../models/genre.model';
import { Subject } from 'rxjs';

@Injectable()
export class GenreService {
  private createSubject = new Subject<Genre>();
  private findAllSubject = new Subject<Genre[]>();
  private findByIdSubject = new Subject<Genre | null>();
  private updateSubject = new Subject<Genre | null>();
  private deleteSubject = new Subject<Genre | null>();

  constructor(@InjectModel('Genre') private readonly genreModel: Model<Genre>) {}

  create(data: Partial<Genre>) {
    this.genreModel.create(data)
      .then(result => this.createSubject.next(result))
      .catch(err => this.createSubject.error(err));
    return this.createSubject.asObservable();
  }

  findAll() {
    this.genreModel.find().exec()
      .then(result => this.findAllSubject.next(result))
      .catch(err => this.findAllSubject.error(err));
    return this.findAllSubject.asObservable();
  }

  findById(id: string) {
    this.genreModel.findById(id).exec()
      .then(result => this.findByIdSubject.next(result))
      .catch(err => this.findByIdSubject.error(err));
    return this.findByIdSubject.asObservable();
  }

  update(id: string, data: Partial<Genre>) {
    this.genreModel.findByIdAndUpdate(id, data, { new: true }).exec()
      .then(result => this.updateSubject.next(result))
      .catch(err => this.updateSubject.error(err));
    return this.updateSubject.asObservable();
  }

  delete(id: string) {
    this.genreModel.findByIdAndDelete(id).exec()
      .then(result => this.deleteSubject.next(result))
      .catch(err => this.deleteSubject.error(err));
    return this.deleteSubject.asObservable();
  }
}
