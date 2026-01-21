'use client';

import React, { useState, useRef, useEffect } from 'react';
import { X, Check, RotateCw, ZoomIn, ZoomOut, Move } from 'lucide-react';

interface ImageCropperProps {
  imageUrl: string;
  onSave: (croppedImageUrl: string) => void;
  onCancel: () => void;
  aspectRatio?: number; // e.g., 16/9, 1, 4/3
}

export function ImageCropper({ imageUrl, onSave, onCancel, aspectRatio }: ImageCropperProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const imageRef = useRef<HTMLImageElement>(null);
  const [crop, setCrop] = useState({ x: 0, y: 0, width: 100, height: 100 });
  const [scale, setScale] = useState(1);
  const [rotation, setRotation] = useState(0);
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [imageLoaded, setImageLoaded] = useState(false);

  useEffect(() => {
    const img = new Image();
    img.src = imageUrl;
    img.onload = () => {
      if (imageRef.current) {
        imageRef.current.src = imageUrl;
        setImageLoaded(true);
        // Initialize crop to center
        const width = aspectRatio ? 200 : 200;
        const height = aspectRatio ? width / aspectRatio : 200;
        setCrop({
          x: (img.width - width) / 2,
          y: (img.height - height) / 2,
          width,
          height,
        });
      }
    };
  }, [imageUrl, aspectRatio]);

  const handleMouseDown = (e: React.MouseEvent) => {
    setIsDragging(true);
    setDragStart({ x: e.clientX - crop.x, y: e.clientY - crop.y });
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDragging || !imageRef.current) return;

    const newX = e.clientX - dragStart.x;
    const newY = e.clientY - dragStart.y;

    setCrop((prev) => ({
      ...prev,
      x: Math.max(0, Math.min(newX, imageRef.current!.width - prev.width)),
      y: Math.max(0, Math.min(newY, imageRef.current!.height - prev.height)),
    }));
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const handleSave = () => {
    if (!canvasRef.current || !imageRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas size to crop size
    canvas.width = crop.width * scale;
    canvas.height = crop.height * scale;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Apply transformations
    ctx.save();
    ctx.translate(canvas.width / 2, canvas.height / 2);
    ctx.rotate((rotation * Math.PI) / 180);
    ctx.scale(scale, scale);
    ctx.translate(-canvas.width / 2, -canvas.height / 2);

    // Draw cropped image
    ctx.drawImage(
      imageRef.current,
      crop.x,
      crop.y,
      crop.width,
      crop.height,
      0,
      0,
      crop.width,
      crop.height
    );

    ctx.restore();

    // Convert to data URL
    const croppedImageUrl = canvas.toDataURL('image/png');
    onSave(croppedImageUrl);
  };

  const handleZoomIn = () => setScale((prev) => Math.min(prev + 0.1, 3));
  const handleZoomOut = () => setScale((prev) => Math.max(prev - 0.1, 0.5));
  const handleRotate = () => setRotation((prev) => (prev + 90) % 360);

  const handleResize = (direction: string, e: React.MouseEvent) => {
    e.stopPropagation();
    const startX = e.clientX;
    const startY = e.clientY;
    const startCrop = { ...crop };

    const handleMove = (moveEvent: MouseEvent) => {
      const deltaX = moveEvent.clientX - startX;
      const deltaY = moveEvent.clientY - startY;

      setCrop((prev) => {
        let newCrop = { ...prev };

        if (direction.includes('e')) {
          newCrop.width = Math.max(50, startCrop.width + deltaX);
        }
        if (direction.includes('w')) {
          const newWidth = Math.max(50, startCrop.width - deltaX);
          newCrop.x = startCrop.x + (startCrop.width - newWidth);
          newCrop.width = newWidth;
        }
        if (direction.includes('s')) {
          newCrop.height = Math.max(50, startCrop.height + deltaY);
        }
        if (direction.includes('n')) {
          const newHeight = Math.max(50, startCrop.height - deltaY);
          newCrop.y = startCrop.y + (startCrop.height - newHeight);
          newCrop.height = newHeight;
        }

        // Maintain aspect ratio if specified
        if (aspectRatio) {
          newCrop.height = newCrop.width / aspectRatio;
        }

        // Keep within bounds
        if (imageRef.current) {
          newCrop.x = Math.max(0, Math.min(newCrop.x, imageRef.current.width - newCrop.width));
          newCrop.y = Math.max(0, Math.min(newCrop.y, imageRef.current.height - newCrop.height));
        }

        return newCrop;
      });
    };

    const handleUp = () => {
      document.removeEventListener('mousemove', handleMove);
      document.removeEventListener('mouseup', handleUp);
    };

    document.addEventListener('mousemove', handleMove);
    document.addEventListener('mouseup', handleUp);
  };

  return (
    <div className="fixed inset-0 bg-black/80 z-[9999] flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="p-4 border-b flex items-center justify-between bg-gray-50">
          <h2 className="text-xl font-semibold">Crop Image</h2>
          <button
            onClick={onCancel}
            className="p-2 hover:bg-gray-200 rounded-full transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Toolbar */}
        <div className="p-4 border-b flex items-center gap-2 bg-gray-50">
          <button
            onClick={handleZoomIn}
            className="px-3 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 flex items-center gap-2"
          >
            <ZoomIn className="w-4 h-4" />
            Zoom In
          </button>
          <button
            onClick={handleZoomOut}
            className="px-3 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 flex items-center gap-2"
          >
            <ZoomOut className="w-4 h-4" />
            Zoom Out
          </button>
          <button
            onClick={handleRotate}
            className="px-3 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 flex items-center gap-2"
          >
            <RotateCw className="w-4 h-4" />
            Rotate
          </button>
          <div className="ml-auto flex items-center gap-2 text-sm text-gray-600">
            <Move className="w-4 h-4" />
            Drag to reposition
          </div>
        </div>

        {/* Canvas Area */}
        <div className="flex-1 overflow-auto bg-gray-100 p-8">
          <div
            className="relative inline-block"
            onMouseMove={handleMouseMove}
            onMouseUp={handleMouseUp}
            onMouseLeave={handleMouseUp}
          >
            <img
              ref={imageRef}
              src={imageUrl}
              alt="Crop preview"
              className="max-w-full h-auto"
              style={{
                transform: `scale(${scale}) rotate(${rotation}deg)`,
                transformOrigin: 'center',
              }}
            />
            {imageLoaded && (
              <div
                className="absolute border-2 border-blue-500 cursor-move shadow-lg"
                style={{
                  left: crop.x,
                  top: crop.y,
                  width: crop.width,
                  height: crop.height,
                  boxShadow: '0 0 0 9999px rgba(0, 0, 0, 0.5)',
                }}
                onMouseDown={handleMouseDown}
              >
                {/* Resize handles */}
                {['nw', 'n', 'ne', 'e', 'se', 's', 'sw', 'w'].map((dir) => (
                  <div
                    key={dir}
                    className="absolute w-3 h-3 bg-white border-2 border-blue-500 cursor-pointer hover:bg-blue-500 transition-colors"
                    style={{
                      top: dir.includes('n') ? -6 : dir.includes('s') ? 'calc(100% - 6px)' : 'calc(50% - 6px)',
                      left: dir.includes('w') ? -6 : dir.includes('e') ? 'calc(100% - 6px)' : 'calc(50% - 6px)',
                      cursor: `${dir}-resize`,
                    }}
                    onMouseDown={(e) => handleResize(dir, e)}
                  />
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t flex items-center justify-between bg-gray-50">
          <div className="text-sm text-gray-600">
            Size: {Math.round(crop.width)} × {Math.round(crop.height)}px | Scale: {scale.toFixed(1)}x | Rotation: {rotation}°
          </div>
          <div className="flex gap-2">
            <button
              onClick={onCancel}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 flex items-center gap-2"
            >
              <Check className="w-4 h-4" />
              Apply
            </button>
          </div>
        </div>
      </div>
      <canvas ref={canvasRef} className="hidden" />
    </div>
  );
}
