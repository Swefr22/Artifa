# 🤖 SWEKEER Chatbot Training System

## Overview
The SWEKEER Chatbot Training system allows **administrators only** to teach the chatbot custom question-answer pairs. This enables the chatbot to provide personalized responses for your festival.

## ✅ Features

### 1. **Add Training Pairs**
- Create custom Q&A pairs for the chatbot
- Categorize with intent types (registration guide, team guide, etc.)
- Add keywords for better matching
- Enable/disable individual pairs
- Use HTML formatting for rich responses

### 2. **Manage Training Data**
- View all training pairs in a searchable database
- Edit existing Q&A pairs
- Delete training pairs
- Track creation date and creator
- Filter by intent and status

### 3. **Intent Categories**
The chatbot supports multiple intent categories for organizing Q&A pairs:
- **registration_guide** - Registration process
- **team_guide** - Team management
- **view_team_guide** - Viewing team information
- **navigation_guide** - Website navigation
- **profile_guide** - Profile management
- **nec_info** - NEC information
- **aids_info** - AIDS Department info
- **artifa_info** - Festival information
- **events** - Event details
- **timeline** - Festival timeline
- **help** - General help
- **custom** - Custom intents

## 🔐 Security

⚠️ **Access Restrictions:**
- **Only administrators and superusers** can access the training page
- Regular users cannot access `/chatbot/training/`
- Training data is stored securely in the database
- All changes are logged with creator information

## 📝 How to Use

### 1. Access the Training Page
```
URL: /chatbot/training/
```

Navigate to the admin dashboard and look for "SWEKEER Chatbot Training" link.

### 2. Add a New Training Pair

**Step 1:** Fill in the Question field
```
"How do I register for ARTIFA FEST?"
```

**Step 2:** Write the Answer
```
<b>Registration Process:</b><br>
1. Go to the Registration page<br>
2. Fill in your details<br>
3. Click Submit<br>
...
```

**Step 3:** Select an Intent (Optional)
```
registration_guide
```

**Step 4:** Add Keywords (Optional)
```
register, registration, sign up, join
```

**Step 5:** Enable/Disable
Check the "Active" checkbox to enable this training pair.

**Step 6:** Save
Click "Save Training Pair" button.

### 3. Edit a Training Pair
1. Click the **Edit** (pencil) icon in the training database
2. Modify the question, answer, or other fields
3. Click "Save Changes"

### 4. Delete a Training Pair
1. Click the **Delete** (trash) icon in the training database
2. Confirm the deletion

## 🎨 HTML Formatting Guide

Your answers can include HTML for better formatting:

| Format | Code | Result |
|--------|------|--------|
| Bold | `<b>Bold Text</b>` | **Bold Text** |
| Strong | `<strong>Strong Text</strong>` | **Strong Text** |
| Line Break | `Text<br>New Line` | Text<br>New Line |
| Italic | `<i>Italic Text</i>` | *Italic Text* |
| Icon | `<i class="fas fa-icon-name"></i>` | Font Awesome Icon |

### Font Awesome Icons

Use any Font Awesome 6.4.0 icon:
```html
<i class="fas fa-check-circle"></i> Success
<i class="fas fa-exclamation-triangle"></i> Warning
<i class="fas fa-users"></i> Team
<i class="fas fa-calendar"></i> Schedule
<i class="fas fa-cog"></i> Settings
```

### Example HTML Answer

```html
<b><i class="fas fa-user-plus"></i> Registration Steps</b><br><br>
<b>Step 1:</b> Visit the Registration Page<br>
<b>Step 2:</b> Enter your register number<br>
<b>Step 3:</b> Fill your personal details<br>
<b>Step 4:</b> Select events<br>
<b>Step 5:</b> Click Submit<br><br>
<i class="fas fa-info-circle"></i> <small>You'll receive a confirmation email</small>
```

## 💾 Database Storage

All training pairs are stored in the `ChatbotTraining` model:

| Field | Type | Description |
|-------|------|-------------|
| `question` | TextField | The user's question |
| `answer` | TextField | The chatbot's response |
| `intent` | CharField | Intent category |
| `keywords` | CharField | Comma-separated keywords |
| `is_active` | BooleanField | Enable/disable toggle |
| `created_at` | DateTimeField | Creation timestamp |
| `updated_at` | DateTimeField | Last update timestamp |
| `created_by` | ForeignKey | Admin who created it |

## 🔍 Search and Filter

The training database includes:
- **Live Search:** Search across questions, answers, and intents
- **Intent Filter:** Filter by intent category
- **Status Filter:** Show active/inactive pairs
- **Sorting:** Click column headers to sort
- **Pagination:** Navigate through large datasets

## 📊 Admin Dashboard Integration

### Via Django Admin
- View all training pairs in `/admin/core/chatbottraining/`
- Add, edit, delete pairs from admin panel
- Filter by intent, status, and date
- Search by question, answer, or keywords

### Via Training Page
- User-friendly interface at `/chatbot/training/`
- Bulk view of all pairs with statistics
- Quick access to edit and delete

## 🧠 How Chatbot Uses Training

1. **User asks a question** in the chatbot
2. **Chatbot checks training database** for matching keywords
3. **If match found:** Returns the training answer (95% confidence)
4. **If no match:** Falls back to spaCy semantic analysis
5. **If still no match:** Returns a help response

### Priority Order
1. Check training Q&A pairs with matching keywords
2. Check guide features (registration, team, etc.)
3. Use spaCy NLP semantic analysis
4. Return general information (events, timeline, etc.)
5. Return help message

## 🚀 Best Practices

✅ **DO:**
- Write clear, concise questions and answers
- Use relevant keywords for each pair
- Test training pairs in the live chatbot
- Keep answers organized with HTML formatting
- Use Font Awesome icons for visual clarity
- Disable old/outdated training pairs
- Review and update training regularly

❌ **DON'T:**
- Write questions that are too generic
- Leave keywords empty for important pairs
- Use only spaCy semantic matching - be explicit with keywords
- Store sensitive information in training answers
- Delete important training pairs without backup
- Share training database access with non-admins

## 📈 Performance Tips

1. **Use Keywords Wisely**
   - Add 3-5 relevant keywords per pair
   - Use common synonyms and variations
   - Include question words (how, what, when, where, why)

2. **Organize with Intents**
   - Group related pairs with same intent
   - Makes maintenance easier
   - Helps analyze chatbot usage

3. **Disable Instead of Delete**
   - Uncheck "Active" instead of deleting
   - Preserves history
   - Easy to reactivate if needed

4. **Regular Review**
   - Check logs for unmatched questions
   - Update training based on user feedback
   - Remove duplicate pairs

## 🐛 Troubleshooting

### Training pair not matching
- Verify keywords are correct
- Check spelling and case sensitivity
- Ensure pair is active (is_active = True)
- Test in chatbot with exact keywords

### Chatbot returns wrong answer
- Check keyword priority (more specific keywords first)
- Ensure no duplicate training pairs
- Verify HTML formatting is correct
- Check if spaCy is overriding the training

### Can't access training page
- Verify you're logged in as admin
- Check user permissions (is_staff = True)
- Ensure `/chatbot/training/` URL is correct
- Check browser cache

## 📝 Example Training Pairs

### Example 1: Registration Guide
**Question:** How do I register for ARTIFA FEST?
**Answer:** 
```html
<b><i class="fas fa-user-plus"></i> Registration Steps</b><br><br>
1. Click on "Register" in the menu<br>
2. Enter your register number<br>
3. Fill in your details<br>
4. Select your events<br>
5. Click Submit<br><br>
<i class="fas fa-info-circle"></i> <small>Confirmation email will be sent</small>
```
**Intent:** registration_guide
**Keywords:** register, registration, signup, join, how to register

### Example 2: Team Management
**Question:** How do I create a team?
**Answer:**
```html
<b><i class="fas fa-users"></i> Create a Team</b><br><br>
1. Login to your account<br>
2. Go to Team Management<br>
3. Click "Create New Team"<br>
4. Enter team name and details<br>
5. Invite members<br>
6. Click Save<br><br>
<b>Tip:</b> Team password is required for members to join!
```
**Intent:** team_guide
**Keywords:** team, create team, manage team, team creation

### Example 3: Event Information
**Question:** When is the festival?
**Answer:**
```html
<b><i class="fas fa-calendar"></i> ARTIFA FEST 2025</b><br><br>
<b>Dates:</b> January 26-27, 2025<br>
<b>Location:</b> NEC Campus<br>
<b>Events:</b> 20+ Technical & Non-Technical events<br><br>
Visit the Schedule page for detailed timeline!
```
**Intent:** artifa_info
**Keywords:** festival, date, when, schedule, artifa

## 📞 Support

For issues or questions about the training system:
1. Check the Django admin logs
2. Verify training pair settings
3. Test in the live chatbot
4. Review HTML formatting

---

**Last Updated:** January 26, 2025
**Version:** 1.0
**Status:** Active ✅
