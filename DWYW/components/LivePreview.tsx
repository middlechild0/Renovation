/**
 * Live Preview Component with Drag & Drop
 * 
 * Renders the template with real-time customizations, drag-and-drop reordering, and inline editing
 */

'use client';

import { useProjectStore } from '@/store/project';
import { EditableText } from '@/components/EditableText';
import { MediaLibrary } from '@/components/MediaLibrary';
import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragEndEvent,
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  useSortable,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { GripVertical, Trash2, Copy, Image as ImageIcon } from 'lucide-react';

export function LivePreview() {
  const { currentProject, design, content, previewMode, updateContent, reorderSections, removeSection, duplicateSection } = useProjectStore();
  const [scale, setScale] = useState(1);
  const [mediaLibraryOpen, setMediaLibraryOpen] = useState(false);
  const [selectedImageField, setSelectedImageField] = useState<{ sectionId: string; field: string } | null>(null);

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  useEffect(() => {
    const updateScale = () => {
      const container = document.getElementById('preview-container');
      if (!container) return;

      const containerWidth = container.clientWidth;
      let targetWidth = 1920;

      if (previewMode === 'tablet') {
        targetWidth = 768;
      } else if (previewMode === 'mobile') {
        targetWidth = 375;
      }

      setScale(Math.min(containerWidth / targetWidth, 1));
    };

    updateScale();
    window.addEventListener('resize', updateScale);
    return () => window.removeEventListener('resize', updateScale);
  }, [previewMode]);

  if (!currentProject || !design) {
    return (
      <div className="h-full flex items-center justify-center bg-gray-100">
        <p className="text-gray-500">Select a template to start designing</p>
      </div>
    );
  }

  const template = currentProject.template;
  const previewWidth = previewMode === 'desktop' ? '100%' : previewMode === 'tablet' ? '768px' : '375px';

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;

    if (over && active.id !== over.id) {
      const sections = template.sections;
      const oldIndex = sections.findIndex((s) => s.id === active.id);
      const newIndex = sections.findIndex((s) => s.id === over.id);
      
      // Store scroll position before reordering
      const container = document.getElementById('preview-container');
      const scrollTop = container?.scrollTop || 0;
      
      reorderSections(oldIndex, newIndex);
      
      // Restore scroll position after DOM update
      requestAnimationFrame(() => {
        if (container) {
          container.scrollTop = scrollTop;
        }
      });
    }
  };

  const handleSelectImage = (sectionId: string, field: string) => {
    setSelectedImageField({ sectionId, field });
    setMediaLibraryOpen(true);
  };

  const handleImageSelected = (url: string) => {
    if (selectedImageField) {
      const sectionContent = content[selectedImageField.sectionId] || {};
      updateContent(selectedImageField.sectionId, {
        ...sectionContent,
        [selectedImageField.field]: url,
      });
    }
    setMediaLibraryOpen(false);
    setSelectedImageField(null);
  };

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(`section-${sectionId}`);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  };

  return (
    <>
      <div
        id="preview-container"
        className="h-full bg-gray-100 overflow-auto flex justify-center p-8"
        style={{ 
          scrollBehavior: 'smooth', 
          overflowY: 'auto', 
          overflowX: 'hidden',
          WebkitOverflowScrolling: 'touch' // Smooth scrolling on iOS
        }}
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3 }}
          style={{
            width: previewWidth,
            maxWidth: '100%',
            transform: `scale(${scale})`,
            transformOrigin: 'top center',
          }}
          className="bg-white shadow-2xl rounded-lg overflow-hidden"
        >
          <style jsx global>{`
            :root {
              --primary-color: ${design.colors.primary};
              --secondary-color: ${design.colors.secondary};
              --accent-color: ${design.colors.accent};
              --background-color: ${design.colors.background};
              --text-color: ${design.colors.text};
              --text-secondary-color: ${design.colors.textSecondary};
              --font-primary: ${design.fonts.primary};
              --font-secondary: ${design.fonts.secondary};
              --font-heading: ${design.fonts.heading};
              --spacing-scale: ${design.spacing};
              --border-radius: ${design.borderRadius}px;
            }

            .preview-content * {
              font-family: var(--font-primary), -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }

            .preview-content h1,
            .preview-content h2,
            .preview-content h3,
            .preview-content h4,
            .preview-content h5,
            .preview-content h6 {
              font-family: var(--font-heading), -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }
          `}</style>

          <div className="preview-content">
            <DndContext
              sensors={sensors}
              collisionDetection={closestCenter}
              onDragEnd={handleDragEnd}
            >
              <SortableContext
                items={template.sections.map((s) => s.id)}
                strategy={verticalListSortingStrategy}
              >
                {template.sections.map((section, index) => (
                  <SortableSection
                    key={section.id}
                    section={section}
                    design={design}
                    content={content[section.id]}
                    index={index}
                    onUpdateContent={(newContent) => updateContent(section.id, newContent)}
                    onRemove={() => removeSection(section.id)}
                    onDuplicate={() => duplicateSection(section.id)}
                    onSelectImage={(field) => handleSelectImage(section.id, field)}
                  />
                ))}
              </SortableContext>
            </DndContext>
          </div>
        </motion.div>
      </div>

      <MediaLibrary
        isOpen={mediaLibraryOpen}
        onClose={() => {
          setMediaLibraryOpen(false);
          setSelectedImageField(null);
        }}
        onSelect={handleImageSelected}
      />
    </>
  );
}

function SortableSection({ section, design, content, index, onUpdateContent, onRemove, onDuplicate, onSelectImage }: any) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: section.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  const [isHovered, setIsHovered] = useState(false);

  const animationVariants = {
    fade: {
      hidden: { opacity: 0 },
      visible: { opacity: 1 },
    },
    slide: {
      hidden: { opacity: 0, y: 50 },
      visible: { opacity: 1, y: 0 },
    },
    bounce: {
      hidden: { opacity: 0, scale: 0.8 },
      visible: { opacity: 1, scale: 1 },
    },
    none: {
      hidden: {},
      visible: {},
    },
  };

  const variant = animationVariants[design.animations.style] || animationVariants.fade;

  return (
    <div
      ref={setNodeRef}
      style={style}
      className="relative group"
      id={`section-${section.id}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <motion.section
        initial={design.animations.enabled ? 'hidden' : 'visible'}
        whileInView="visible"
        viewport={{ once: true, margin: '-100px' }}
        transition={{ duration: 0.6, delay: index * 0.1 }}
        variants={variant}
        style={{
          padding: `calc(3rem * ${design.spacing})`,
        }}
      >
        {/* Render section based on type */}
        {section.type === 'hero' && <HeroSection section={section} design={design} content={content} onUpdateContent={onUpdateContent} onSelectImage={onSelectImage} />}
        {section.type === 'features' && <FeaturesSection section={section} design={design} content={content} onUpdateContent={onUpdateContent} />}
        {section.type === 'pricing' && <PricingSection section={section} design={design} content={content} onUpdateContent={onUpdateContent} />}
        {section.type === 'testimonials' && <TestimonialsSection section={section} design={design} content={content} onUpdateContent={onUpdateContent} />}
        {section.type === 'cta' && <CTASection section={section} design={design} content={content} onUpdateContent={onUpdateContent} />}
        {section.type === 'gallery' && <GallerySection section={section} design={design} content={content} onSelectImage={onSelectImage} />}
        {section.type === 'contact' && <ContactSection section={section} design={design} content={content} onUpdateContent={onUpdateContent} />}
        {section.type === 'footer' && <FooterSection section={section} design={design} content={content} onUpdateContent={onUpdateContent} />}
      </motion.section>

      {/* Section Controls */}
      {isHovered && (
        <div className="absolute top-2 right-2 flex items-center space-x-2 bg-white/90 backdrop-blur-sm rounded-lg shadow-lg p-2 z-10">
          <button
            {...listeners}
            {...attributes}
            className="p-2 hover:bg-gray-100 rounded cursor-grab active:cursor-grabbing"
            title="Drag to reorder"
          >
            <GripVertical size={16} />
          </button>
          <button
            onClick={onDuplicate}
            className="p-2 hover:bg-gray-100 rounded"
            title="Duplicate section"
          >
            <Copy size={16} />
          </button>
          <button
            onClick={onRemove}
            className="p-2 hover:bg-red-50 text-red-600 rounded"
            title="Delete section"
          >
            <Trash2 size={16} />
          </button>
        </div>
      )}
    </div>
  );
}

// Section Components with Inline Editing
function HeroSection({ section, design, content, onUpdateContent, onSelectImage }: any) {
  return (
    <div className="text-center max-w-4xl mx-auto">
      <EditableText
        value={content?.headline || 'Welcome to Your Site'}
        onChange={(value) => onUpdateContent({ ...content, headline: value })}
        className="text-6xl font-bold mb-6"
        style={{ color: design.colors.text }}
        as="h1"
      />
      <EditableText
        value={content?.subheadline || 'Build something amazing with our platform'}
        onChange={(value) => onUpdateContent({ ...content, subheadline: value })}
        className="text-xl mb-8"
        style={{ color: design.colors.textSecondary }}
        as="p"
      />
      <button
        className="px-8 py-4 text-white font-semibold text-lg transition-transform hover:scale-105"
        style={{
          backgroundColor: design.colors.primary,
          borderRadius: `${design.borderRadius}px`,
        }}
      >
        <EditableText
          value={content?.ctaText || 'Get Started'}
          onChange={(value) => onUpdateContent({ ...content, ctaText: value })}
          className="inline-block"
          as="span"
        />
      </button>
      
      {content?.heroImage && (
        <div className="mt-8 relative group">
          <img src={content.heroImage} alt="Hero" className="w-full rounded-lg" />
          <button
            onClick={() => onSelectImage('heroImage')}
            className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center"
          >
            <ImageIcon className="text-white" size={48} />
          </button>
        </div>
      )}
      {!content?.heroImage && (
        <button
          onClick={() => onSelectImage('heroImage')}
          className="mt-8 w-full aspect-video border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center hover:border-gray-400 hover:bg-gray-50 transition-colors"
        >
          <div className="text-center">
            <ImageIcon className="mx-auto mb-2 text-gray-400" size={48} />
            <p className="text-gray-600">Click to add hero image</p>
          </div>
        </button>
      )}
    </div>
  );
}

function FeaturesSection({ section, design, content, onUpdateContent }: any) {
  const features = content?.features || [
    { title: 'Feature 1', description: 'Amazing feature description' },
    { title: 'Feature 2', description: 'Another great feature' },
    { title: 'Feature 3', description: 'Even more features' },
  ];

  return (
    <div>
      <EditableText
        value={content?.title || 'Features'}
        onChange={(value) => onUpdateContent({ ...content, title: value })}
        className="text-4xl font-bold text-center mb-12"
        style={{ color: design.colors.text }}
        as="h2"
      />
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {features.map((feature: any, index: number) => (
          <div
            key={index}
            className="p-6"
            style={{
              backgroundColor: design.colors.background,
              borderRadius: `${design.borderRadius}px`,
              border: `1px solid ${design.colors.textSecondary}20`,
            }}
          >
            <EditableText
              value={feature.title}
              onChange={(value) => {
                const newFeatures = [...features];
                newFeatures[index] = { ...feature, title: value };
                onUpdateContent({ ...content, features: newFeatures });
              }}
              className="text-xl font-bold mb-3"
              style={{ color: design.colors.text }}
              as="h3"
            />
            <EditableText
              value={feature.description}
              onChange={(value) => {
                const newFeatures = [...features];
                newFeatures[index] = { ...feature, description: value };
                onUpdateContent({ ...content, features: newFeatures });
              }}
              style={{ color: design.colors.textSecondary }}
              multiline
              as="p"
            />
          </div>
        ))}
      </div>
    </div>
  );
}

function PricingSection({ section, design, content, onUpdateContent }: any) {
  const plans = content?.plans || [
    { name: 'Basic', price: '$9', features: ['Feature 1', 'Feature 2', 'Feature 3'] },
    { name: 'Pro', price: '$29', features: ['Everything in Basic', 'Feature 4', 'Feature 5'] },
    { name: 'Enterprise', price: '$99', features: ['Everything in Pro', 'Feature 6', 'Feature 7'] },
  ];

  return (
    <div>
      <EditableText
        value={content?.title || 'Pricing'}
        onChange={(value) => onUpdateContent({ ...content, title: value })}
        className="text-4xl font-bold text-center mb-12"
        style={{ color: design.colors.text }}
        as="h2"
      />
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
        {plans.map((plan: any, index: number) => (
          <div
            key={index}
            className="p-8 text-center"
            style={{
              backgroundColor: design.colors.background,
              borderRadius: `${design.borderRadius}px`,
              border: `2px solid ${index === 1 ? design.colors.primary : design.colors.textSecondary}20`,
            }}
          >
            <EditableText
              value={plan.name}
              onChange={(value) => {
                const newPlans = [...plans];
                newPlans[index] = { ...plan, name: value };
                onUpdateContent({ ...content, plans: newPlans });
              }}
              className="text-2xl font-bold mb-4"
              style={{ color: design.colors.text }}
              as="h3"
            />
            <div className="mb-6">
              <EditableText
                value={plan.price}
                onChange={(value) => {
                  const newPlans = [...plans];
                  newPlans[index] = { ...plan, price: value };
                  onUpdateContent({ ...content, plans: newPlans });
                }}
                className="text-5xl font-bold inline-block"
                style={{ color: design.colors.primary }}
                as="span"
              />
              <span style={{ color: design.colors.textSecondary }}>/month</span>
            </div>
            <ul className="space-y-3 mb-8">
              {plan.features.map((feature: string, i: number) => (
                <li key={i} style={{ color: design.colors.textSecondary }}>
                  ✓ {feature}
                </li>
              ))}
            </ul>
            <button
              className="w-full py-3 font-semibold"
              style={{
                backgroundColor: index === 1 ? design.colors.primary : 'transparent',
                color: index === 1 ? 'white' : design.colors.primary,
                border: `2px solid ${design.colors.primary}`,
                borderRadius: `${design.borderRadius}px`,
              }}
            >
              Choose Plan
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

function TestimonialsSection({ section, design, content, onUpdateContent }: any) {
  const testimonials = content?.testimonials || [
    { author: 'John Doe', role: 'CEO, Company', text: 'Amazing product!' },
    { author: 'Jane Smith', role: 'Designer', text: 'Love the interface!' },
  ];

  return (
    <div>
      <EditableText
        value={content?.title || 'Testimonials'}
        onChange={(value) => onUpdateContent({ ...content, title: value })}
        className="text-4xl font-bold text-center mb-12"
        style={{ color: design.colors.text }}
        as="h2"
      />
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
        {testimonials.map((testimonial: any, index: number) => (
          <div
            key={index}
            className="p-6"
            style={{
              backgroundColor: design.colors.background,
              borderRadius: `${design.borderRadius}px`,
              border: `1px solid ${design.colors.textSecondary}20`,
            }}
          >
            <EditableText
              value={testimonial.text}
              onChange={(value) => {
                const newTestimonials = [...testimonials];
                newTestimonials[index] = { ...testimonial, text: value };
                onUpdateContent({ ...content, testimonials: newTestimonials });
              }}
              className="mb-4 text-lg"
              style={{ color: design.colors.text }}
              multiline
              as="p"
            />
            <div>
              <EditableText
                value={testimonial.author}
                onChange={(value) => {
                  const newTestimonials = [...testimonials];
                  newTestimonials[index] = { ...testimonial, author: value };
                  onUpdateContent({ ...content, testimonials: newTestimonials });
                }}
                className="font-bold"
                style={{ color: design.colors.text }}
                as="p"
              />
              <EditableText
                value={testimonial.role}
                onChange={(value) => {
                  const newTestimonials = [...testimonials];
                  newTestimonials[index] = { ...testimonial, role: value };
                  onUpdateContent({ ...content, testimonials: newTestimonials });
                }}
                style={{ color: design.colors.textSecondary }}
                as="p"
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function CTASection({ section, design, content, onUpdateContent }: any) {
  return (
    <div
      className="text-center py-20 px-8"
      style={{
        backgroundColor: design.colors.primary,
        borderRadius: `${design.borderRadius}px`,
      }}
    >
      <EditableText
        value={content?.headline || 'Ready to Get Started?'}
        onChange={(value) => onUpdateContent({ ...content, headline: value })}
        className="text-4xl font-bold text-white mb-4"
        as="h2"
      />
      <EditableText
        value={content?.subheadline || 'Join thousands of satisfied customers'}
        onChange={(value) => onUpdateContent({ ...content, subheadline: value })}
        className="text-xl text-white/90 mb-8"
        as="p"
      />
      <button
        className="px-8 py-4 bg-white font-semibold text-lg"
        style={{
          color: design.colors.primary,
          borderRadius: `${design.borderRadius}px`,
        }}
      >
        <EditableText
          value={content?.ctaText || 'Sign Up Now'}
          onChange={(value) => onUpdateContent({ ...content, ctaText: value })}
          as="span"
        />
      </button>
    </div>
  );
}

function GallerySection({ section, design, content, onSelectImage }: any) {
  return (
    <div>
      <h2
        className="text-4xl font-bold text-center mb-12"
        style={{ color: design.colors.text }}
      >
        {content?.title || 'Gallery'}
      </h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
          <button
            key={i}
            onClick={() => onSelectImage(`gallery${i}`)}
            className="aspect-square bg-gray-200 hover:bg-gray-300 transition-colors flex items-center justify-center group"
            style={{ borderRadius: `${design.borderRadius}px` }}
          >
            <ImageIcon className="text-gray-400 group-hover:text-gray-500" size={32} />
          </button>
        ))}
      </div>
    </div>
  );
}

function ContactSection({ section, design, content, onUpdateContent }: any) {
  return (
    <div className="max-w-2xl mx-auto">
      <EditableText
        value={content?.title || 'Contact Us'}
        onChange={(value) => onUpdateContent({ ...content, title: value })}
        className="text-4xl font-bold text-center mb-12"
        style={{ color: design.colors.text }}
        as="h2"
      />
      <form className="space-y-6">
        <input
          type="text"
          placeholder="Name"
          className="w-full px-4 py-3 border"
          style={{
            borderRadius: `${design.borderRadius}px`,
            borderColor: design.colors.textSecondary,
          }}
        />
        <input
          type="email"
          placeholder="Email"
          className="w-full px-4 py-3 border"
          style={{
            borderRadius: `${design.borderRadius}px`,
            borderColor: design.colors.textSecondary,
          }}
        />
        <textarea
          placeholder="Message"
          rows={5}
          className="w-full px-4 py-3 border"
          style={{
            borderRadius: `${design.borderRadius}px`,
            borderColor: design.colors.textSecondary,
          }}
        />
        <button
          type="submit"
          className="w-full py-3 text-white font-semibold"
          style={{
            backgroundColor: design.colors.primary,
            borderRadius: `${design.borderRadius}px`,
          }}
        >
          Send Message
        </button>
      </form>
    </div>
  );
}

function FooterSection({ section, design, content, onUpdateContent }: any) {
  return (
    <div
      className="text-center py-8 border-t"
      style={{ borderColor: design.colors.textSecondary + '20' }}
    >
      <EditableText
        value={content?.copyright || '© 2024 Your Company. All rights reserved.'}
        onChange={(value) => onUpdateContent({ ...content, copyright: value })}
        style={{ color: design.colors.textSecondary }}
        as="p"
      />
    </div>
  );
}
