/**
 * Editable Text Component
 * 
 * Click-to-edit inline text with ContentEditable
 */

'use client';

import { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';

interface EditableTextProps {
  value: string;
  onChange: (value: string) => void;
  className?: string;
  placeholder?: string;
  multiline?: boolean;
  as?: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6' | 'p' | 'span';
}

export function EditableText({
  value,
  onChange,
  className = '',
  placeholder = 'Click to edit',
  multiline = false,
  as: Component = 'p',
}: EditableTextProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [localValue, setLocalValue] = useState(value);
  const ref = useRef<HTMLElement>(null);

  useEffect(() => {
    setLocalValue(value);
  }, [value]);

  useEffect(() => {
    if (isEditing && ref.current) {
      ref.current.focus();
      // Select all text
      const range = document.createRange();
      range.selectNodeContents(ref.current);
      const selection = window.getSelection();
      selection?.removeAllRanges();
      selection?.addRange(range);
    }
  }, [isEditing]);

  const handleBlur = () => {
    setIsEditing(false);
    if (localValue !== value) {
      onChange(localValue);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (!multiline && e.key === 'Enter') {
      e.preventDefault();
      ref.current?.blur();
    }
    if (e.key === 'Escape') {
      setLocalValue(value);
      ref.current?.blur();
    }
  };

  const handleInput = (e: React.FormEvent<HTMLElement>) => {
    const newValue = e.currentTarget.textContent || '';
    setLocalValue(newValue);
  };

  return (
    <div
      className={`relative inline-block w-full ${isEditing ? 'ring-2 ring-blue-500 ring-offset-2 rounded z-50' : 'z-10'}`}
      onClick={(e) => {
        if (!isEditing) {
          e.stopPropagation();
          setIsEditing(true);
        }
      }}
    >
      <Component
        ref={ref as any}
        contentEditable={isEditing}
        suppressContentEditableWarning
        onBlur={handleBlur}
        onKeyDown={handleKeyDown}
        onInput={handleInput}
        onClick={(e) => {
          if (isEditing) {
            e.stopPropagation();
          }
        }}
        className={`${className} ${
          isEditing ? 'outline-none bg-white' : 'cursor-text hover:bg-blue-50/30 transition-colors'
        } ${!localValue ? 'text-gray-400' : ''}`}
        style={{ minHeight: '1em', position: 'relative' }}
      >
        {localValue || placeholder}
      </Component>
      {!isEditing && (
        <div className="absolute top-0 right-0 px-2 py-1 bg-blue-500 text-white text-xs rounded-bl opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
          ✏️
        </div>
      )}
    </div>
  );
}
