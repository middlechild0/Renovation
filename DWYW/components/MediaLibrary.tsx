/**
 * Media Library Component
 * 
 * Upload, manage, and select images for the website
 */

'use client';

import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { X, Upload, Image as ImageIcon, Trash2, Check, Crop } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { ImageCropper } from './ImageCropper';

interface MediaFile {
  id: string;
  url: string;
  name: string;
  size: number;
  type: string;
  uploadedAt: Date;
}

interface MediaLibraryProps {
  isOpen: boolean;
  onClose: () => void;
  onSelect: (url: string) => void;
  allowMultiple?: boolean;
}

export function MediaLibrary({ isOpen, onClose, onSelect, allowMultiple = false }: MediaLibraryProps) {
  const [files, setFiles] = useState<MediaFile[]>(() => {
    // Load from localStorage
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('dwyw-media-library');
      if (saved) {
        return JSON.parse(saved).map((f: any) => ({
          ...f,
          uploadedAt: new Date(f.uploadedAt),
        }));
      }
    }
    return [];
  });
  const [selectedFiles, setSelectedFiles] = useState<Set<string>>(new Set());
  const [uploading, setUploading] = useState(false);
  const [cropImage, setCropImage] = useState<{ url: string; id: string } | null>(null);

  const saveToStorage = (newFiles: MediaFile[]) => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('dwyw-media-library', JSON.stringify(newFiles));
    }
  };

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    setUploading(true);

    try {
      const newFiles: MediaFile[] = await Promise.all(
        acceptedFiles.map(async (file) => {
          // Convert to base64 for localStorage (in production, upload to cloud storage)
          const reader = new FileReader();
          const dataUrl = await new Promise<string>((resolve) => {
            reader.onload = () => resolve(reader.result as string);
            reader.readAsDataURL(file);
          });

          return {
            id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
            url: dataUrl,
            name: file.name,
            size: file.size,
            type: file.type,
            uploadedAt: new Date(),
          };
        })
      );

      const updatedFiles = [...files, ...newFiles];
      setFiles(updatedFiles);
      saveToStorage(updatedFiles);
    } finally {
      setUploading(false);
    }
  }, [files]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'],
    },
    multiple: true,
  });

  const handleDelete = (id: string) => {
    const updatedFiles = files.filter((f) => f.id !== id);
    setFiles(updatedFiles);
    saveToStorage(updatedFiles);
    selectedFiles.delete(id);
    setSelectedFiles(new Set(selectedFiles));
  };

  const handleCrop = (file: MediaFile) => {
    setCropImage({ url: file.url, id: file.id });
  };

  const handleCropSave = (croppedUrl: string) => {
    if (!cropImage) return;
    
    const updatedFiles = files.map((f) =>
      f.id === cropImage.id ? { ...f, url: croppedUrl } : f
    );
    setFiles(updatedFiles);
    saveToStorage(updatedFiles);
    setCropImage(null);
  };

  const handleSelect = (file: MediaFile) => {
    if (allowMultiple) {
      const newSelected = new Set(selectedFiles);
      if (newSelected.has(file.id)) {
        newSelected.delete(file.id);
      } else {
        newSelected.add(file.id);
      }
      setSelectedFiles(newSelected);
    } else {
      onSelect(file.url);
      onClose();
    }
  };

  const handleConfirmSelection = () => {
    if (allowMultiple && selectedFiles.size > 0) {
      const selectedUrls = files
        .filter((f) => selectedFiles.has(f.id))
        .map((f) => f.url);
      // For now, just select the first one (in future, support multiple)
      onSelect(selectedUrls[0]);
    }
    onClose();
  };

  if (!isOpen) return null;

  return (
    <>
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center">
        {/* Backdrop */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="absolute inset-0 bg-black/50"
        />

        {/* Modal */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          className="relative bg-white rounded-xl shadow-2xl w-full max-w-5xl max-h-[80vh] overflow-hidden flex flex-col"
        >
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-gray-200">
            <div>
              <h2 className="text-2xl font-bold">Media Library</h2>
              <p className="text-sm text-gray-600 mt-1">
                {files.length} file{files.length !== 1 ? 's' : ''} • {selectedFiles.size} selected
              </p>
            </div>
            <button
              onClick={onClose}
              className="w-10 h-10 flex items-center justify-center rounded-full hover:bg-gray-100"
            >
              <X size={20} />
            </button>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto p-6">
            {/* Upload Area */}
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-xl p-8 mb-6 text-center cursor-pointer transition-all ${
                isDragActive
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-300 hover:border-gray-400 hover:bg-gray-50'
              }`}
            >
              <input {...getInputProps()} />
              <Upload className="mx-auto mb-4 text-gray-400" size={48} />
              {uploading ? (
                <p className="text-lg font-medium text-gray-900">Uploading...</p>
              ) : isDragActive ? (
                <p className="text-lg font-medium text-blue-600">Drop images here</p>
              ) : (
                <>
                  <p className="text-lg font-medium text-gray-900 mb-2">
                    Drag & drop images here
                  </p>
                  <p className="text-sm text-gray-600">
                    or click to browse • PNG, JPG, GIF, WebP, SVG
                  </p>
                </>
              )}
            </div>

            {/* Files Grid */}
            {files.length === 0 ? (
              <div className="text-center py-12">
                <ImageIcon className="mx-auto mb-4 text-gray-300" size={64} />
                <p className="text-gray-600">No images yet. Upload some to get started!</p>
              </div>
            ) : (
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {files.map((file) => (
                  <motion.div
                    key={file.id}
                    layout
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.8 }}
                    className="relative group"
                  >
                    <div
                      onClick={() => handleSelect(file)}
                      className={`aspect-square rounded-lg overflow-hidden cursor-pointer border-2 transition-all ${
                        selectedFiles.has(file.id)
                          ? 'border-blue-500 ring-2 ring-blue-200'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <img
                        src={file.url}
                        alt={file.name}
                        className="w-full h-full object-cover"
                      />
                      {selectedFiles.has(file.id) && (
                        <div className="absolute inset-0 bg-blue-500/20 flex items-center justify-center">
                          <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                            <Check size={20} className="text-white" />
                          </div>
                        </div>
                      )}
                    </div>

                    {/* File Info */}
                    <div className="mt-2">
                      <p className="text-sm font-medium truncate">{file.name}</p>
                      <p className="text-xs text-gray-500">
                        {(file.size / 1024).toFixed(1)} KB
                      </p>
                    </div>

                    {/* Action Buttons */}
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleCrop(file);
                      }}
                      className="absolute top-2 left-2 w-8 h-8 bg-blue-500 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center hover:bg-blue-600"
                      title="Crop image"
                    >
                      <Crop size={16} />
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDelete(file.id);
                      }}
                      className="absolute top-2 right-2 w-8 h-8 bg-red-500 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center hover:bg-red-600"
                      title="Delete image"
                    >
                      <Trash2 size={16} />
                    </button>
                  </motion.div>
                ))}
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="p-6 border-t border-gray-200 flex items-center justify-between">
            <button
              onClick={onClose}
              className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              Cancel
            </button>
            {allowMultiple && selectedFiles.size > 0 && (
              <button
                onClick={handleConfirmSelection}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                Select {selectedFiles.size} Image{selectedFiles.size !== 1 ? 's' : ''}
              </button>
            )}
          </div>
        </motion.div>
      </div>
    </AnimatePresence>

    {/* Image Cropper Modal */}
    {cropImage && (
      <ImageCropper
        imageUrl={cropImage.url}
        onSave={handleCropSave}
        onCancel={() => setCropImage(null)}
      />
    )}
    </>
  );
}
