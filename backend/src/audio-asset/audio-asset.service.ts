
import { Injectable } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { AudioAsset } from '../models/audio-asset.model';
import { ReplaySubject } from 'rxjs';


/**
 * Service for managing audio assets in the database.
 * Provides CRUD operations using RxJS hot observables.
 *
 * Usage:
 *   Inject AudioAssetService and call methods for asset management.
 */
@Injectable()
export class AudioAssetService {

  /**
   * Injects the AudioAsset Mongoose model.
   * @param audioAssetModel Mongoose model for AudioAsset
   */
  constructor(@InjectModel('AudioAsset') private readonly audioAssetModel: Model<AudioAsset>) {}

  /**
   * Create a new audio asset.
   * @param data Partial audio asset data
   * @returns Observable emitting the created asset
   */
  create(data: Partial<AudioAsset>) {
    this.audioAssetModel.create(data)
    const subject = new ReplaySubject(1);
    this.audioAssetModel.create(data)
      .then(result => {
        subject.next(result);
        subject.complete();
      })
      .catch(err => subject.error(err));
    return subject.asObservable();
  }

  /**
   * Find all audio assets.
   * @returns Observable emitting array of assets
   */
  findAll() {
    this.audioAssetModel.find().populate('genre').populate('vocalFeatures').exec()
    const subject = new ReplaySubject(1);
    this.audioAssetModel.find().populate('genre').populate('vocalFeatures').exec()
      .then(result => {
        subject.next(result);
        subject.complete();
      })
      .catch(err => subject.error(err));
    return subject.asObservable();
  }

  /**
   * Find an audio asset by ID.
   * @param id Asset ID
   * @returns Observable emitting the found asset or null
   */
  findById(id: string) {
    this.audioAssetModel.findById(id).populate('genre').populate('vocalFeatures').exec()
    const subject = new ReplaySubject(1);
    this.audioAssetModel.findById(id).populate('genre').populate('vocalFeatures').exec()
      .then(result => {
        subject.next(result);
        subject.complete();
      })
      .catch(err => subject.error(err));
    return subject.asObservable();
  }

  /**
   * Update an audio asset by ID.
   * @param id Asset ID
   * @param data Partial asset data
   * @returns Observable emitting the updated asset or null
   */
  update(id: string, data: Partial<AudioAsset>) {
    this.audioAssetModel.findByIdAndUpdate(id, data, { new: true }).exec()
    const subject = new ReplaySubject(1);
    this.audioAssetModel.findByIdAndUpdate(id, data, { new: true }).exec()
      .then(result => {
        subject.next(result);
        subject.complete();
      })
      .catch(err => subject.error(err));
    return subject.asObservable();
  }

  /**
   * Delete an audio asset by ID.
   * @param id Asset ID
   * @returns Observable emitting the deleted asset or null
   */
  delete(id: string) {
    this.audioAssetModel.findByIdAndDelete(id).exec()
    const subject = new ReplaySubject(1);
    this.audioAssetModel.findByIdAndDelete(id).exec()
      .then(result => {
        subject.next(result);
        subject.complete();
      })
      .catch(err => subject.error(err));
    return subject.asObservable();
  }
}
