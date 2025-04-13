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
   - Keep `tsconfig.json` in the root directory
   - Use proper path aliases for imports (`@/components/`)
   - Don't remove TypeScript configuration without verification
   - Ensure path aliases match the actual file structure

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

## Deployment and Build
1. **Build Configuration**
   - Keep `next.config.mjs` in the frontend directory
   - Configure proper module resolution in `tsconfig.json`
   - Ensure all UI components are properly exported
   - Test builds locally before deployment

2. **Vercel Deployment**
   - Configure proper build settings in `vercel.json`
   - Ensure all dependencies are listed in `package.json`
   - Check for any missing UI components
   - Verify path aliases in production build

3. **Common Build Issues**
   - ❌ Missing UI components in production
   - ❌ Incorrect path aliases in `tsconfig.json`
   - ❌ Missing dependencies in `package.json`
   - ✅ Test builds locally first
   - ✅ Keep UI components in sync with imports
   - ✅ Verify all path aliases are correct

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

4. **Deployment**
   - ❌ Don't deploy without local testing
   - ❌ Don't ignore build warnings
   - ❌ Don't modify production config without testing
   - ✅ Test all changes locally first
   - ✅ Keep deployment config up to date
   - ✅ Monitor build logs for errors 