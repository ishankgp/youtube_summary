# Cursor Rules for YouTube Summary Project

## Formatting Rules

### Text Formatting
1. **Section Headers**
   - ONLY section headers should be in bold
   - Key points, quotes, and other content should NOT be in bold
   - Use `#` for main sections, `##` for subsections

2. **Transcript Display**
   - Only show translated transcript when available
   - Do not display original transcripts
   - Keep language indicator for context

3. **Summary Sections**
   - Section titles: Bold
   - Content: Regular weight
   - Lists: Regular weight with proper indentation
   - Quotes: Italic, not bold

### Component Structure
1. **File Organization**
   - Components in `/components` directory
   - Utilities in `/lib` directory
   - Pages in `/app` directory
   - Types in separate `.d.ts` files

2. **Component Naming**
   - PascalCase for component names
   - Descriptive and purpose-indicating names
   - Suffix with type (e.g., Button, Card, etc.)

## Code Style

### TypeScript
1. **Types and Interfaces**
   - Define interfaces for all props
   - Use TypeScript generics when appropriate
   - Export types when shared across components

2. **State Management**
   - Use hooks for local state
   - Avoid prop drilling
   - Keep state close to where it's used

### React Best Practices
1. **Component Structure**
   - One component per file
   - Clear separation of concerns
   - Proper use of hooks
   - Consistent error handling

2. **Performance**
   - Memoize expensive computations
   - Use proper key props in lists
   - Avoid unnecessary re-renders

## Error Handling
1. **API Errors**
   - Clear error messages
   - User-friendly error states
   - Proper error boundaries

2. **Input Validation**
   - Validate URLs before processing
   - Show clear validation feedback
   - Handle edge cases gracefully

## Accessibility
1. **General**
   - Proper ARIA labels
   - Keyboard navigation
   - Color contrast compliance

2. **Interactive Elements**
   - Clear focus states
   - Proper button roles
   - Loading state indicators

## Common Mistakes to Avoid
1. **Formatting**
   - ❌ Don't make key points bold
   - ❌ Don't bold list items
   - ❌ Don't show duplicate transcripts
   - ✅ Only bold section headers

2. **Component Logic**
   - ❌ Don't mix presentation and business logic
   - ❌ Don't use inline styles (use Tailwind)
   - ✅ Use proper TypeScript types
   - ✅ Handle loading states properly 