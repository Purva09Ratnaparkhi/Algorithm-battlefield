# 🔒 Category Locking System - Complete Guide

## Overview

**Player 2 is now FORCED to use the same category as Player 1.**

When Player 1 selects a category, Player 2 cannot select any other category. All other categories are locked and disabled for Player 2.

---

## How It Works

### Step-by-Step Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Player 1 selects a category (e.g., "Sorting")            │
│    ✓ Player 1 category = "Sorting"                          │
│    ✓ Player 2's view updates                                │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Player 2's UI now shows:                                 │
│    • Sorting card: 🔒 FORCED (bright green glow)            │
│    • All other cards: 🚫 LOCKED (faded red)                 │
│    • Player 2 can ONLY click on Sorting                     │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Player 2 clicks on Sorting                               │
│    ✓ Player 2 category = "Sorting"                          │
│    ✓ Next button is enabled                                 │
│    ✓ Both players confirmed same category                   │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Click "Next" to proceed to Algorithm Selection           │
│    • Both players see algorithms in Sorting category        │
└─────────────────────────────────────────────────────────────┘
```

---

## Visual Changes

### Player 2's Category Cards

#### Before Selection (Player 1 hasn't selected yet)
```
┌─────────────────┐
│  🔄 SORTING     │  ← Can click
│                 │
└─────────────────┘
```

#### After Player 1 Selects "Sorting"

**Player 1's Side:**
```
┌─────────────────┐
│  ✓ SORTING      │  ← Selected (red glow)
│                 │
└─────────────────┘
```

**Player 2's Side:**
```
┌──────────────────────┐
│  🔒 SORTING          │  ← FORCED (green glow)
│       🔒 FORCED      │    Can click to confirm
└──────────────────────┘

┌──────────────────────┐
│  🚫 SEARCHING        │  ← LOCKED (faded out)
│       🚫 LOCKED      │    Cannot click
└──────────────────────┘

┌──────────────────────┐
│  🚫 SHORTEST PATH    │  ← LOCKED (faded out)
│       🚫 LOCKED      │    Cannot click
└──────────────────────┘
```

---

## Backend Validation

### `app.py` Changes

```python
@app.route('/select_category', methods=['GET', 'POST'])
def select_category():
    """Category Selection - Player 1 chooses, Player 2 must use same category"""
    
    if player == 1:
        # ✓ Player 1 can select ANY category
        session['category_p1'] = category
        
    elif player == 2:
        # ✓ Player 2 can ONLY select Player 1's category
        p1_category = session.get('category_p1')
        
        if not p1_category:
            # Error: Player 1 hasn't selected yet
            return error("Player 1 must select a category first")
        
        if category != p1_category:
            # Error: Player 2 tried to select different category
            return error(f"Player 2 must use Player 1's category: {p1_category}")
        
        session['category_p2'] = category
```

**Validation Rules:**
1. ✅ Player 1 selects any category → Success
2. ✅ Player 2 tries to select Player 1's category → Success
3. ❌ Player 2 tries to select different category → Error
4. ❌ Player 2 tries to select before Player 1 → Error

---

## Frontend Behavior

### `select_category.html` Changes

**Rendering Logic:**
```javascript
categories.forEach(cat => {
    // If Player 1 selected "Sorting"
    if (cat === "Sorting") {
        // Show as FORCED for Player 2
        p2Card.className = 'category-card selected forced';
        p2Card.innerHTML += '<small>🔒 FORCED</small>';
        p2Card.addEventListener('click', selectCategory);
    } else {
        // Show as LOCKED for Player 2
        p2Card.className = 'category-card locked disabled';
        p2Card.innerHTML += '<small>🚫 LOCKED</small>';
        p2Card.style.cursor = 'not-allowed';
        // No event listener
    }
});
```

**Next Button Logic:**
```javascript
function checkNextButton() {
    // Before: selectedP1 !== selectedP2 (different categories)
    // Now: selectedP1 === selectedP2 (SAME category)
    
    if (selectedP1 && selectedP2 && selectedP1 === selectedP2) {
        nextBtn.disabled = false;  // ✓ Enable Next
    } else {
        nextBtn.disabled = true;   // ✗ Disable Next
    }
}
```

---

## CSS Styling

### Card States

```css
/* FORCED - Player 2's must-select option */
.category-card.forced {
    background: rgba(0, 255, 150, 0.2);        /* Green glow */
    border-color: rgba(0, 255, 150, 0.6);
    box-shadow: 0 0 20px rgba(0, 255, 150, 0.4);
    cursor: pointer;
}

/* LOCKED - Player 2's disabled options */
.category-card.locked,
.category-card.disabled {
    opacity: 0.35;                              /* Faded */
    cursor: not-allowed;
    background: rgba(255, 100, 100, 0.1);      /* Red overlay */
    border-color: rgba(255, 100, 100, 0.2);
}
```

---

## User Experience

### Player 1's Perspective
```
"Choose your category wisely!"

┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  SORTING     │  │  SEARCHING   │  │ SHORTEST ... │
│  (can click) │  │  (can click) │  │  (can click) │
└──────────────┘  └──────────────┘  └──────────────┘

→ I select "SORTING"
```

### Player 2's Perspective
```
"Your opponent chose! Use the same category."

┌─────────────────┐  ┌────────────────┐  ┌────────────────┐
│  🔒 SORTING     │  │  🚫 SEARCHING  │  │  🚫 SHORTEST..│
│  🔒 FORCED      │  │  🚫 LOCKED     │  │  🚫 LOCKED    │
│  (must click)   │  │  (disabled)    │  │  (disabled)   │
└─────────────────┘  └────────────────┘  └────────────────┘

→ I click "SORTING" to confirm
```

---

## Error Handling

### Scenario 1: Player 2 tries to select before Player 1
```
Backend Response:
{
    success: false,
    message: "Player 1 must select a category first"
}
```

### Scenario 2: Player 2 tries to select different category
```
Backend Response:
{
    success: false,
    message: "Player 2 must use Player 1's category: sorting"
}
```

### Scenario 3: Both select same category
```
Backend Response:
{
    success: true,
    message: "Category confirmed for Player 2"
}

Frontend Action:
→ Next button enabled
→ Proceed to /select_algorithm
```

---

## Frequently Asked Questions

### Q: Can Player 2 choose a different category?
**A:** No. Player 2 is forced to use Player 1's selected category.

### Q: What happens if Player 1 changes their selection?
**A:** Player 2's UI updates immediately. All cards re-render with new locking state.

### Q: Can Player 1 change their selection after Player 2 confirms?
**A:** Yes, but Player 2 would need to re-confirm. The session is updated in real-time.

### Q: How many categories can be locked for Player 2?
**A:** 7 out of 8 (all except Player 1's chosen category).

### Q: Is this validated on the backend?
**A:** Yes! Both frontend (UI) and backend (API) enforce this rule.

---

## Testing the Feature

### Test Case 1: Normal Flow
```
1. Player 1 clicks "Sorting"
   Expected: Sorting card shows red glow with ✓
   
2. Player 2 sees Sorting as FORCED (green glow)
   Expected: All other cards show 🚫 LOCKED (faded)
   
3. Player 2 clicks "Sorting"
   Expected: Next button enabled
   
4. Click "Next"
   Expected: Proceed to /select_algorithm
```

### Test Case 2: Player 2 Tries to Cheat
```
1. Player 1 clicks "Sorting"
2. Player 2 tries to click "Searching"
   Expected: No event listener, card doesn't respond
   Expected: Frontend silently prevents action
```

### Test Case 3: Backend Validation
```
1. Player 1 clicks "Sorting"
2. Manually send AJAX request: Player 2 selects "Searching"
   Expected: Backend returns error
   Expected: message: "Player 2 must use Player 1's category: sorting"
```

---

## Code Changes Summary

| File | Change | Impact |
|------|--------|--------|
| `app.py` | Player 2 category validation | Enforces same category on backend |
| `select_category.html` | Forced/locked rendering | Shows UI feedback |
| `select_category.html` | Event listener filtering | Prevents Player 2 from clicking locked cards |
| `select_category.html` | Next button logic | Requires `selectedP1 === selectedP2` |
| `select_category.html` | CSS styling | Visual distinction for forced/locked states |

---

## Backward Compatibility

✅ **No breaking changes**
- Existing sessions automatically work with new logic
- Old data cleared on homepage refresh
- New locking enforced from first page load

---

## Files Modified

```
✓ app.py (backend validation)
✓ templates/select_category.html (frontend UI + logic)
```

---

## Summary

🔒 **Category Locking Feature:**
- Player 1 selects any category
- Player 2 forced to use Player 1's category
- 7 categories locked for Player 2
- 1 category (forced) highlighted in green
- Validated on both frontend and backend
- Cannot be bypassed or cheated

**Status:** ✅ Fully Implemented & Ready to Test

---
