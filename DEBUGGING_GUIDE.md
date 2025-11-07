# 🔍 Debugging Guide - Next Button Not Clickable

## Quick Troubleshooting Checklist

### ✅ Step 1: Open Browser Developer Tools
```
Press: F12 or Ctrl+Shift+I
Go to: Console tab
```

### ✅ Step 2: Check Console for Initialization Messages
You should see:
```
Page initialized with: {selectedP1: '', selectedP2: ''}
✗ Next button DISABLED
```

### ✅ Step 3: Select a Category for Player 1
Click on any category card in Player 1's section.

**Expected Console Output:**
```
Player 1 selecting: sorting
Selection successful: {success: true, message: "Category selected for Player 1"}
✓ Player 1 selected: sorting
✗ Next button DISABLED (because Player 2 hasn't selected yet)
```

**What should change on screen:**
- ✅ Player 1's card shows red glow (selected)
- ✅ Player 1's badge updates to "SORTING"
- ✅ Player 2's cards update:
  - "Sorting" card glows green with "🔒 FORCED" label
  - All other cards fade out with "🚫 LOCKED" label

### ✅ Step 4: Select Category for Player 2
Click on Player 2's FORCED category (should be the same as Player 1's).

**Expected Console Output:**
```
Player 2 selecting: sorting
Selection successful: {success: true, message: "Category confirmed for Player 2"}
✓ Player 2 selected: sorting
Checking next button... {selectedP1: 'sorting', selectedP2: 'sorting', isSame: true}
✓ Next button ENABLED
```

**What should change on screen:**
- ✅ Player 2's badge updates to "SORTING"
- ✅ Next button changes from DISABLED to ENABLED
- ✅ Next button cursor changes to pointer

### ✅ Step 5: Click Next Button
Now the Next button should be clickable!

**Expected Action:**
```
Next button clicked {selectedP1: 'sorting', selectedP2: 'sorting'}
Navigating to /select_algorithm
→ Page redirects to /select_algorithm
```

---

## Common Issues & Solutions

### Issue 1: Next Button Still Disabled After Both Select
**Cause:** Player 1 and Player 2 selections don't match

**Solution:**
```javascript
// Open console and check:
console.log(selectedP1, selectedP2)
// Should output: "sorting" "sorting"  (identical)

// NOT: "sorting" "Sorting"  (case mismatch)
// NOT: "sorting" ""  (empty)
```

---

### Issue 2: Player 2 Can Click Locked Cards
**Cause:** Event listener not properly removed

**Solution:**
1. Hard refresh page: `Ctrl+F5`
2. Clear browser cache
3. Check console for errors

**Verify in Console:**
```javascript
// Should show all cards
document.querySelectorAll('.category-card')

// Check locked cards
document.querySelectorAll('.category-card.locked')
// Should have cursor: not-allowed style
```

---

### Issue 3: Selection Request Fails
**Cause:** Backend error or validation failed

**Expected Error Messages in Console:**
```
Selection failed: ...
Response: {"success": false, "message": "..."}
```

**Common Backend Errors:**
1. `"Player 1 must select a category first"` 
   - → Player 2 tried selecting before Player 1
   
2. `"Player 2 must use Player 1's category: sorting"`
   - → Player 2 tried selecting different category

---

### Issue 4: Selections Revert or Change Unexpectedly
**Cause:** Session expired or page reloaded

**Solution:**
1. Start fresh: Click "Back to Home" button
2. Session clears automatically
3. Try again from step 1

---

## Manual Testing Commands

### Test 1: Check Page State
```javascript
// In Console, type:
console.log({selectedP1, selectedP2})
console.log(document.getElementById('nextBtn').disabled)
```

### Test 2: Force Enable Button
```javascript
// In Console, type (for testing only):
document.getElementById('nextBtn').disabled = false
```

### Test 3: Manually Simulate Player 1 Selection
```javascript
// In Console, type:
selectedP1 = 'sorting'
renderCategories()
checkNextButton()
```

### Test 4: Manually Simulate Player 2 Selection
```javascript
// In Console, type:
selectedP2 = 'sorting'
renderCategories()
checkNextButton()
```

### Test 5: Check Next Button Click Handler
```javascript
// In Console, type:
document.getElementById('nextBtn').click()
// Should navigate if both selected
```

---

## Browser Inspector Checks

### Check 1: Button HTML
```html
<!-- Open Inspector (F12), find button with id="nextBtn" -->
<!-- Should look like: -->
<button id="nextBtn" class="btn btn-danger btn-lg">
    Next <i class="fas fa-arrow-right"></i>
</button>
```

### Check 2: Button CSS State
```
1. Open Inspector
2. Click on the button
3. Look at Styles panel
4. Check computed CSS for "disabled" pseudo-class
5. Should show opacity/pointer-events changes
```

### Check 3: Network Requests
```
1. Open Inspector → Network tab
2. Clear any existing requests
3. Click Player 1's category card
4. Should see POST request to /select_category
5. Check Response tab
6. Should see: {"success": true, "message": "..."}
```

---

## Files Involved in Button Logic

| File | Role | Lines |
|------|------|-------|
| `select_category.html` | Button definition & click handler | 50-80 |
| `select_category.html` | JavaScript logic | 80-210 |
| `app.py` | Backend validation | 88-130 |

---

## Complete Flow Diagram

```
START
  ↓
[Load Page]
  ↓
  selectedP1 = "" (empty)
  selectedP2 = "" (empty)
  ✗ Next Button DISABLED
  ↓
[Player 1 Clicks Category]
  ↓
  → AJAX POST /select_category (player=1, category="sorting")
  → Backend accepts any category
  → Success: selectedP1 = "sorting"
  → renderCategories() called
  → checkNextButton() called
  ✗ Next Button still DISABLED (Player 2 not selected yet)
  ↓
[Player 2 Sees Updated UI]
  ↓
  → Player 1's category (sorting) shown as 🔒 FORCED (green)
  → All other categories shown as 🚫 LOCKED (faded)
  ↓
[Player 2 Clicks FORCED Category]
  ↓
  → AJAX POST /select_category (player=2, category="sorting")
  → Backend validates: category === Player1's category ✓
  → Success: selectedP2 = "sorting"
  → renderCategories() called
  → checkNextButton() called
  ✓ Next Button ENABLED (both selected same category!)
  ↓
[Player Clicks Next Button]
  ↓
  → window.location.href = '/select_algorithm'
  → Redirects to algorithm selection page
END
```

---

## Real-Time Debugging

### Monitor Button State
```javascript
// Paste in console and keep it running:
setInterval(() => {
    console.log('Button Status:', {
        disabled: document.getElementById('nextBtn').disabled,
        selectedP1: selectedP1,
        selectedP2: selectedP2,
        match: selectedP1 === selectedP2
    });
}, 1000);
```

### Watch for Changes
```javascript
// Paste in console to see all updates:
const observer = new MutationObserver(() => {
    console.log('DOM changed!', {selectedP1, selectedP2});
});
observer.observe(document.body, {subtree: true, childList: true});
```

---

## Network Debugging

### View All Requests
```
1. F12 → Network tab
2. Select XHR (to see only AJAX)
3. Make selections
4. Should see POST requests to /select_category
5. Check each request's Response
```

### Expected Response Format
```json
{
    "success": true,
    "message": "Category selected for Player 1"
}
```

---

## CSS Validation

### Check Button Styles
```css
/* Button should have */
#nextBtn {
    cursor: pointer;  /* when enabled */
}

#nextBtn:disabled {
    opacity: 0.5;
    cursor: not-allowed;  /* when disabled */
}
```

### Check Card Styles
```css
.category-card.forced {
    background: rgba(0, 255, 150, 0.2);     /* green glow */
    box-shadow: 0 0 20px rgba(0, 255, 150, 0.4);
}

.category-card.locked {
    opacity: 0.35;                           /* faded */
    cursor: not-allowed;
}
```

---

## Session Validation

### Check Session Data
```python
# Add this temporarily to app.py to see session:
@app.route('/debug_session')
def debug_session():
    return jsonify(dict(session))
```

Then visit: `http://localhost:5000/debug_session`

Should show:
```json
{
    "category_p1": "sorting",
    "category_p2": "sorting"
}
```

---

## Final Verification Checklist

- [ ] Console shows initialization messages
- [ ] Player 1 selection shows success message
- [ ] Cards update with forced/locked states
- [ ] Player 2's forced card shows green glow
- [ ] Player 2's locked cards show faded
- [ ] Player 2 selection shows success message
- [ ] Console shows button enabled message
- [ ] Button visual state changes (not grayed out)
- [ ] Button cursor is pointer (not forbidden)
- [ ] Clicking button redirects to /select_algorithm

---

## Need More Help?

### Enable Extra Verbose Logging
Add this to the top of the script block in `select_category.html`:
```javascript
const DEBUG = true;  // Set to true for extra logging

function log(...args) {
    if (DEBUG) console.log('[DEBUG]', ...args);
}
```

Then replace all `console.log` with `log()`.

---

**Last Updated:** November 6, 2025
**Status:** Active Debugging Guide
