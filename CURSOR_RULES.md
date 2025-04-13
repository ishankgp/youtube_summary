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
   - UI components in `/components/ui` directory
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

## Configuration and Dependencies
1. **TypeScript Configuration**
   - Keep `tsconfig.json` as the main TypeScript config
   - Use proper path aliases for imports (`@/components/`)
   - Don't remove TypeScript configuration without verification

2. **Dependency Management**
   - Check component usage before removing dependencies
   - Keep UI dependencies in sync with component usage
   - Test builds locally before pushing changes
   - Document all major dependency changes

3. **Import Rules**
   - Use `@/components/ui/` for UI component imports
   - Use `@/lib/` for utility functions
   - Use `@/app/` for page components
   - Verify import paths match file structure

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

3. **Configuration**
   - ❌ Don't remove dependencies without checking usage
   - ❌ Don't modify import paths without updating config
   - ❌ Don't change TypeScript config without testing
   - ✅ Verify all changes locally before pushing
   - ✅ Keep UI dependencies in sync with components 