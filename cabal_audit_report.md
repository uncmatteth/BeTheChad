# Code Audit Report: Cabal Feature
Generated on: 2025-03-12 09:02:09

## Summary
- Total Files: 13
- Total Lines: 4025
  - Code: 3085 (76.6%)
  - Comments: 314 (7.8%)
  - Blank: 626 (15.6%)
- Average Lines per File: 309.6
- Issues Found:
  - Security Issues: 10
  - Code Smells: 77
  - Best Practice Violations: 3824

## File Types
- .py: 7 files
- .html: 6 files

## Files Analyzed
- app\controllers\cabal.py
- app\models\cabal.py
- app\templates\cabal\all_battles.html
- app\templates\cabal\battles.html
- app\templates\cabal\edit.html
- app\templates\cabal\index.html
- app\templates\cabal\leaderboard.html
- app\templates\cabal\schedule_battle.html
- app\utils\bot_commands.py
- tests\test_cabal_mock.py
- tests\test_cabal_model.py
- tests\test_cabal_routes.py
- tests\test_cabal_simplified.py

## Issues by File

### app\controllers\cabal.py (615 issues)

#### Security Issues
- Line 95: Form data without validation
  `name = request.form.get('name', '').strip()`
- Line 96: Form data without validation
  `description = request.form.get('description', '').strip()`
- Line 156: Form data without validation
  `invite_code = request.form.get('invite_code', '').strip()`
- Line 244: Form data without validation
  `name = request.form.get('name', '').strip()`
- Line 245: Form data without validation
  `description = request.form.get('description', '').strip()`
- Line 383: Form data without validation
  `chad_id = request.form.get('chad_id', '').strip()`
- Line 384: Form data without validation
  `role_type = request.form.get('role_type', '').strip()`
- Line 469: Form data without validation
  `opponent_cabal_id = request.form.get('opponent_cabal_id', '').strip()`
- Line 470: Form data without validation
  `battle_date = request.form.get('battle_date', '').strip()`
- Line 471: Form data without validation
  `battle_time = request.form.get('battle_time', '').strip()`

#### Code Smells
- Line 9: Debug print statement
  `cabal_bp = Blueprint('cabal', __name__)`
- Line 135: Explicit commit - check transaction management
  `db.session.commit()`
- Line 274: Explicit commit - check transaction management
  `db.session.commit()`
- Line 509: Datetime usage - check for timezone awareness
  `if scheduled_at <= datetime.utcnow():`

#### Best Practice Violations
- Line 13: Function without docstring
  `def index():`
- Line 92: Function without docstring
  `def create():`
- Line 147: Function without docstring
  `def join():`
- Line 214: Function without docstring
  `def leave(cabal_id):`
- Line 234: Function without docstring
  `def edit(cabal_id):`
- Line 283: Function without docstring
  `def battles(cabal_id):`
- Line 294: Function without docstring
  `def remove_member(cabal_id):`
- Line 324: Function without docstring
  `def promote_leader(cabal_id):`
- Line 354: Function without docstring
  `def disband(cabal_id):`
- Line 374: Function without docstring
  `def appoint_officer(cabal_id):`
- Line 413: Function without docstring
  `def remove_officer(cabal_id, role_type):`
- Line 439: Function without docstring
  `def vote_remove_leader(cabal_id):`
- Line 459: Function without docstring
  `def schedule_battle(cabal_id):`
- Line 542: Function without docstring
  `def opt_into_battle(battle_id):`
- Line 568: Function without docstring
  `def all_battles():`
- Line 613: Function without docstring
  `def leaderboard():`
- Line 108: Using len() in comparison - use implicit truthiness
  `if len(name) > 50:`
- Line 112: Using len() in comparison - use implicit truthiness
  `if len(description) > 500:`
- Line 167: Using len() in comparison - use implicit truthiness
  `if len(invite_code) != 6 or not re.match(r'^[A-Z0-9]+$', invite_code):`
- Line 192: Using len() in comparison - use implicit truthiness
  `if len(code) != 6 or not re.match(r'^[A-Z0-9]+$', code):`
- Line 257: Using len() in comparison - use implicit truthiness
  `if len(name) > 50:`
- Line 261: Using len() in comparison - use implicit truthiness
  `if len(description) > 500:`
- Line 14: Indentation over 4 spaces
  `"""Display the user's cabal"""`
- Line 15: Indentation over 4 spaces
  `cabals = Cabal.query.filter_by(leader_id=current_user.chad.id).all()`
- Line 16: Indentation over 4 spaces
  ``
- Line 17: Indentation over 4 spaces
  `# Also check if user is a member of a cabal`
- Line 18: Indentation over 4 spaces
  `cabal_member = CabalMember.query.filter_by(chad_id=current_user.chad.id).first()`
- Line 19: Indentation over 4 spaces
  `if cabal_member:`
- Line 20: Indentation over 4 spaces
  `cabal = cabal_member.cabal`
- Line 21: Indentation over 4 spaces
  ``
- Line 22: Indentation over 4 spaces
  `# Get officers`
- Line 23: Indentation over 4 spaces
  `officers = {}`
- Line 24: Indentation over 4 spaces
  `for role_type in ['clout', 'roast_level', 'cringe_resistance', 'drip_factor']:`
- Line 25: Indentation over 4 spaces
  `officer_role = cabal.get_officer(role_type)`
- Line 26: Indentation over 4 spaces
  `if officer_role:`
- Line 27: Indentation over 4 spaces
  `from app.models.chad import Chad`
- Line 28: Indentation over 4 spaces
  `officer_chad = Chad.query.get(officer_role.chad_id)`
- Line 29: Indentation over 4 spaces
  `if officer_chad:`
- Line 30: Indentation over 4 spaces
  `from app.models.user import User`
- Line 31: Indentation over 4 spaces
  `officer_user = User.query.filter_by(chad_id=officer_chad.id).first()`
- Line 32: Indentation over 4 spaces
  `officers[role_type] = {`
- Line 33: Indentation over 4 spaces
  `'id': officer_chad.id,`
- Line 34: Indentation over 4 spaces
  `'name': officer_chad.name,`
- Line 35: Indentation over 4 spaces
  `'username': officer_user.twitter_handle if officer_user else 'Unknown',`
- Line 36: Indentation over 4 spaces
  `'title': cabal.get_officer_title(role_type)`
- Line 37: Indentation over 4 spaces
  `}`
- Line 38: Indentation over 4 spaces
  ``
- Line 39: Indentation over 4 spaces
  `# Get vote counts for leader removal`
- Line 40: Indentation over 4 spaces
  `leader_removal_votes = CabalVote.query.filter_by(`
- Line 41: Indentation over 4 spaces
  `cabal_id=cabal.id,`
- Line 42: Indentation over 4 spaces
  `vote_type='remove_leader',`
- Line 43: Indentation over 4 spaces
  `target_id=cabal.leader_id`
- Line 44: Indentation over 4 spaces
  `).count()`
- Line 45: Indentation over 4 spaces
  ``
- Line 46: Indentation over 4 spaces
  `active_members_count = cabal.get_active_member_count()`
- Line 47: Indentation over 4 spaces
  `removal_vote_percentage = (leader_removal_votes / active_members_count * 100) if active_members_count > 0 else 0`
- Line 48: Indentation over 4 spaces
  ``
- Line 49: Indentation over 4 spaces
  `# Get scheduled battles`
- Line 50: Indentation over 4 spaces
  `upcoming_battles = CabalBattle.query.filter_by(`
- Line 51: Indentation over 4 spaces
  `cabal_id=cabal.id,`
- Line 52: Indentation over 4 spaces
  `completed=False`
- Line 53: Indentation over 4 spaces
  `).filter(`
- Line 54: Indentation over 4 spaces
  `CabalBattle.scheduled_at > datetime.utcnow()`
- Line 55: Indentation over 4 spaces
  `).order_by(CabalBattle.scheduled_at).all()`
- Line 56: Indentation over 4 spaces
  ``
- Line 57: Indentation over 4 spaces
  `# Check if user has voted for leader removal`
- Line 58: Indentation over 4 spaces
  `user_voted = CabalVote.query.filter_by(`
- Line 59: Indentation over 4 spaces
  `cabal_id=cabal.id,`
- Line 60: Indentation over 4 spaces
  `voter_id=current_user.chad.id,`
- Line 61: Indentation over 4 spaces
  `vote_type='remove_leader',`
- Line 62: Indentation over 4 spaces
  `target_id=cabal.leader_id`
- Line 63: Indentation over 4 spaces
  `).first() is not None`
- Line 64: Indentation over 4 spaces
  ``
- Line 65: Indentation over 4 spaces
  `# Add current datetime for template`
- Line 66: Indentation over 4 spaces
  `now = datetime.utcnow()`
- Line 67: Indentation over 4 spaces
  ``
- Line 68: Indentation over 4 spaces
  `# Get leader information`
- Line 69: Indentation over 4 spaces
  `from app.models.chad import Chad`
- Line 70: Indentation over 4 spaces
  `from app.models.user import User`
- Line 71: Indentation over 4 spaces
  ``
- Line 72: Indentation over 4 spaces
  `leader = Chad.query.get(cabal.leader_id)`
- Line 73: Indentation over 4 spaces
  `if leader:`
- Line 74: Indentation over 4 spaces
  `leader.user = User.query.filter_by(chad_id=leader.id).first()`
- Line 75: Indentation over 4 spaces
  ``
- Line 76: Indentation over 4 spaces
  `cabal.leader = leader`
- Line 77: Indentation over 4 spaces
  ``
- Line 78: Indentation over 4 spaces
  `return render_template('cabal/index.html',`
- Line 79: Indentation over 4 spaces
  `cabal=cabal,`
- Line 80: Indentation over 4 spaces
  `officers=officers,`
- Line 81: Indentation over 4 spaces
  `leader_removal_votes=leader_removal_votes,`
- Line 82: Indentation over 4 spaces
  `removal_vote_percentage=removal_vote_percentage,`
- Line 83: Indentation over 4 spaces
  `upcoming_battles=upcoming_battles,`
- Line 84: Indentation over 4 spaces
  `user_voted=user_voted,`
- Line 85: Indentation over 4 spaces
  `is_leader=(cabal.leader_id == current_user.chad.id),`
- Line 86: Indentation over 4 spaces
  `now=now)`
- Line 87: Indentation over 4 spaces
  ``
- Line 88: Indentation over 4 spaces
  `return render_template('cabal/index.html', cabal=None)`
- Line 93: Indentation over 4 spaces
  `"""Create a new cabal"""`
- Line 94: Indentation over 4 spaces
  `if request.method == 'POST':`
- Line 95: Indentation over 4 spaces
  `name = request.form.get('name', '').strip()`
- Line 96: Indentation over 4 spaces
  `description = request.form.get('description', '').strip()`
- Line 97: Indentation over 4 spaces
  ``
- Line 98: Indentation over 4 spaces
  `# Validate input`
- Line 99: Indentation over 4 spaces
  `if not name:`
- Line 100: Indentation over 4 spaces
  `flash('Cabal name is required', 'danger')`
- Line 101: Indentation over 4 spaces
  `return redirect(url_for('cabal.create'))`
- Line 102: Indentation over 4 spaces
  ``
- Line 103: Indentation over 4 spaces
  `# Sanitize inputs`
- Line 104: Indentation over 4 spaces
  `name = escape(name)`
- Line 105: Indentation over 4 spaces
  `description = escape(description)`
- Line 106: Indentation over 4 spaces
  ``
- Line 107: Indentation over 4 spaces
  `# Check length constraints`
- Line 108: Indentation over 4 spaces
  `if len(name) > 50:`
- Line 109: Indentation over 4 spaces
  `flash('Cabal name must be 50 characters or less', 'danger')`
- Line 110: Indentation over 4 spaces
  `return redirect(url_for('cabal.create'))`
- Line 111: Indentation over 4 spaces
  ``
- Line 112: Indentation over 4 spaces
  `if len(description) > 500:`
- Line 113: Indentation over 4 spaces
  `flash('Description is too long (max 500 characters)', 'danger')`
- Line 114: Indentation over 4 spaces
  `return redirect(url_for('cabal.create'))`
- Line 115: Indentation over 4 spaces
  ``
- Line 116: Indentation over 4 spaces
  `# Check if name is already taken`
- Line 117: Indentation over 4 spaces
  `existing_cabal = Cabal.query.filter_by(name=name).first()`
- Line 118: Indentation over 4 spaces
  `if existing_cabal:`
- Line 119: Indentation over 4 spaces
  `flash('A cabal with this name already exists', 'danger')`
- Line 120: Indentation over 4 spaces
  `return redirect(url_for('cabal.create'))`
- Line 121: Indentation over 4 spaces
  ``
- Line 122: Indentation over 4 spaces
  `# Check if user is already in a cabal`
- Line 123: Indentation over 4 spaces
  `existing_membership = CabalMember.query.filter_by(chad_id=current_user.chad.id).first()`
- Line 124: Indentation over 4 spaces
  `if existing_membership:`
- Line 125: Indentation over 4 spaces
  `flash('You are already in a cabal', 'danger')`
- Line 126: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 127: Indentation over 4 spaces
  ``
- Line 128: Indentation over 4 spaces
  `cabal = Cabal(`
- Line 129: Indentation over 4 spaces
  `name=name,`
- Line 130: Indentation over 4 spaces
  `description=description,`
- Line 131: Indentation over 4 spaces
  `leader_id=current_user.chad.id`
- Line 132: Indentation over 4 spaces
  `)`
- Line 133: Indentation over 4 spaces
  ``
- Line 134: Indentation over 4 spaces
  `db.session.add(cabal)`
- Line 135: Indentation over 4 spaces
  `db.session.commit()`
- Line 136: Indentation over 4 spaces
  ``
- Line 137: Indentation over 4 spaces
  `# Add the leader as a member`
- Line 138: Indentation over 4 spaces
  `cabal.add_member(current_user.chad.id)`
- Line 139: Indentation over 4 spaces
  ``
- Line 140: Indentation over 4 spaces
  `flash('Cabal created successfully', 'success')`
- Line 141: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 142: Indentation over 4 spaces
  ``
- Line 143: Indentation over 4 spaces
  `return render_template('cabal/create.html')`
- Line 148: Indentation over 4 spaces
  `"""Join an existing cabal"""`
- Line 149: Indentation over 4 spaces
  `# Check if user is already in a cabal`
- Line 150: Indentation over 4 spaces
  `existing_membership = CabalMember.query.filter_by(chad_id=current_user.chad.id).first()`
- Line 151: Indentation over 4 spaces
  `if existing_membership:`
- Line 152: Indentation over 4 spaces
  `flash('You are already in a cabal', 'danger')`
- Line 153: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 154: Indentation over 4 spaces
  ``
- Line 155: Indentation over 4 spaces
  `if request.method == 'POST':`
- Line 156: Indentation over 4 spaces
  `invite_code = request.form.get('invite_code', '').strip()`
- Line 157: Indentation over 4 spaces
  ``
- Line 158: Indentation over 4 spaces
  `# Validate input`
- Line 159: Indentation over 4 spaces
  `if not invite_code:`
- Line 160: Indentation over 4 spaces
  `flash('Invite code is required', 'danger')`
- Line 161: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 162: Indentation over 4 spaces
  ``
- Line 163: Indentation over 4 spaces
  `# Sanitize input`
- Line 164: Indentation over 4 spaces
  `invite_code = escape(invite_code)`
- Line 165: Indentation over 4 spaces
  ``
- Line 166: Indentation over 4 spaces
  `# Validate format (alphanumeric, 6 chars)`
- Line 167: Indentation over 4 spaces
  `if len(invite_code) != 6 or not re.match(r'^[A-Z0-9]+$', invite_code):`
- Line 168: Indentation over 4 spaces
  `flash('Invalid invite code format', 'danger')`
- Line 169: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 170: Indentation over 4 spaces
  ``
- Line 171: Indentation over 4 spaces
  `cabal = Cabal.query.filter_by(invite_code=invite_code).first()`
- Line 172: Indentation over 4 spaces
  ``
- Line 173: Indentation over 4 spaces
  `if not cabal:`
- Line 174: Indentation over 4 spaces
  `flash('Invalid invite code', 'danger')`
- Line 175: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 176: Indentation over 4 spaces
  ``
- Line 177: Indentation over 4 spaces
  `success, message = cabal.add_member(current_user.chad.id)`
- Line 178: Indentation over 4 spaces
  ``
- Line 179: Indentation over 4 spaces
  `if success:`
- Line 180: Indentation over 4 spaces
  `flash('You have joined the cabal successfully', 'success')`
- Line 181: Indentation over 4 spaces
  `else:`
- Line 182: Indentation over 4 spaces
  `flash(message, 'danger')`
- Line 183: Indentation over 4 spaces
  ``
- Line 184: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 185: Indentation over 4 spaces
  ``
- Line 186: Indentation over 4 spaces
  `# Handle GET with code param (from invitation link)`
- Line 187: Indentation over 4 spaces
  `code = request.args.get('code')`
- Line 188: Indentation over 4 spaces
  `if code:`
- Line 189: Indentation over 4 spaces
  `# Sanitize and validate input`
- Line 190: Indentation over 4 spaces
  `code = escape(code.strip())`
- Line 191: Indentation over 4 spaces
  ``
- Line 192: Indentation over 4 spaces
  `if len(code) != 6 or not re.match(r'^[A-Z0-9]+$', code):`
- Line 193: Indentation over 4 spaces
  `flash('Invalid invite code format', 'danger')`
- Line 194: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 195: Indentation over 4 spaces
  ``
- Line 196: Indentation over 4 spaces
  `cabal = Cabal.query.filter_by(invite_code=code).first()`
- Line 197: Indentation over 4 spaces
  ``
- Line 198: Indentation over 4 spaces
  `if cabal:`
- Line 199: Indentation over 4 spaces
  `success, message = cabal.add_member(current_user.chad.id)`
- Line 200: Indentation over 4 spaces
  ``
- Line 201: Indentation over 4 spaces
  `if success:`
- Line 202: Indentation over 4 spaces
  `flash('You have joined the cabal successfully', 'success')`
- Line 203: Indentation over 4 spaces
  `else:`
- Line 204: Indentation over 4 spaces
  `flash(message, 'danger')`
- Line 205: Indentation over 4 spaces
  ``
- Line 206: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 207: Indentation over 4 spaces
  `else:`
- Line 208: Indentation over 4 spaces
  `flash('Invalid invite code', 'danger')`
- Line 209: Indentation over 4 spaces
  ``
- Line 210: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 215: Indentation over 4 spaces
  `"""Leave a cabal"""`
- Line 216: Indentation over 4 spaces
  `cabal = Cabal.query.get_or_404(cabal_id)`
- Line 217: Indentation over 4 spaces
  ``
- Line 218: Indentation over 4 spaces
  `# Cannot leave if you're the leader`
- Line 219: Indentation over 4 spaces
  `if cabal.leader_id == current_user.chad.id:`
- Line 220: Indentation over 4 spaces
  `flash('The cabal leader cannot leave. Disband the cabal or transfer leadership first.', 'danger')`
- Line 221: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 222: Indentation over 4 spaces
  ``
- Line 223: Indentation over 4 spaces
  `success, message = cabal.remove_member(current_user.chad.id)`
- Line 224: Indentation over 4 spaces
  ``
- Line 225: Indentation over 4 spaces
  `if success:`
- Line 226: Indentation over 4 spaces
  `flash('You have left the cabal', 'success')`
- Line 227: Indentation over 4 spaces
  `else:`
- Line 228: Indentation over 4 spaces
  `flash(message, 'danger')`
- Line 229: Indentation over 4 spaces
  ``
- Line 230: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 235: Indentation over 4 spaces
  `"""Edit cabal details"""`
- Line 236: Indentation over 4 spaces
  `cabal = Cabal.query.get_or_404(cabal_id)`
- Line 237: Indentation over 4 spaces
  ``
- Line 238: Indentation over 4 spaces
  `# Only leader can edit`
- Line 239: Indentation over 4 spaces
  `if cabal.leader_id != current_user.chad.id:`
- Line 240: Indentation over 4 spaces
  `flash('Only the cabal leader can edit cabal details', 'danger')`
- Line 241: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 242: Indentation over 4 spaces
  ``
- Line 243: Indentation over 4 spaces
  `if request.method == 'POST':`
- Line 244: Indentation over 4 spaces
  `name = request.form.get('name', '').strip()`
- Line 245: Indentation over 4 spaces
  `description = request.form.get('description', '').strip()`
- Line 246: Indentation over 4 spaces
  ``
- Line 247: Indentation over 4 spaces
  `# Validate input`
- Line 248: Indentation over 4 spaces
  `if not name:`
- Line 249: Indentation over 4 spaces
  `flash('Cabal name is required', 'danger')`
- Line 250: Indentation over 4 spaces
  `return redirect(url_for('cabal.edit', cabal_id=cabal_id))`
- Line 251: Indentation over 4 spaces
  ``
- Line 252: Indentation over 4 spaces
  `# Sanitize inputs`
- Line 253: Indentation over 4 spaces
  `name = escape(name)`
- Line 254: Indentation over 4 spaces
  `description = escape(description)`
- Line 255: Indentation over 4 spaces
  ``
- Line 256: Indentation over 4 spaces
  `# Check length constraints`
- Line 257: Indentation over 4 spaces
  `if len(name) > 50:`
- Line 258: Indentation over 4 spaces
  `flash('Cabal name must be 50 characters or less', 'danger')`
- Line 259: Indentation over 4 spaces
  `return redirect(url_for('cabal.edit', cabal_id=cabal_id))`
- Line 260: Indentation over 4 spaces
  ``
- Line 261: Indentation over 4 spaces
  `if len(description) > 500:`
- Line 262: Indentation over 4 spaces
  `flash('Description is too long (max 500 characters)', 'danger')`
- Line 263: Indentation over 4 spaces
  `return redirect(url_for('cabal.edit', cabal_id=cabal_id))`
- Line 264: Indentation over 4 spaces
  ``
- Line 265: Indentation over 4 spaces
  `# Check if name is already taken by a different cabal`
- Line 266: Indentation over 4 spaces
  `existing_cabal = Cabal.query.filter(Cabal.name == name, Cabal.id != cabal.id).first()`
- Line 267: Indentation over 4 spaces
  `if existing_cabal:`
- Line 268: Indentation over 4 spaces
  `flash('A cabal with this name already exists', 'danger')`
- Line 269: Indentation over 4 spaces
  `return redirect(url_for('cabal.edit', cabal_id=cabal_id))`
- Line 270: Indentation over 4 spaces
  ``
- Line 271: Indentation over 4 spaces
  `cabal.name = name`
- Line 272: Indentation over 4 spaces
  `cabal.description = description`
- Line 273: Indentation over 4 spaces
  ``
- Line 274: Indentation over 4 spaces
  `db.session.commit()`
- Line 275: Indentation over 4 spaces
  ``
- Line 276: Indentation over 4 spaces
  `flash('Cabal updated successfully', 'success')`
- Line 277: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 278: Indentation over 4 spaces
  ``
- Line 279: Indentation over 4 spaces
  `return render_template('cabal/edit.html', cabal=cabal)`
- Line 284: Indentation over 4 spaces
  `"""View cabal battles"""`
- Line 285: Indentation over 4 spaces
  `cabal = Cabal.query.get_or_404(cabal_id)`
- Line 286: Indentation over 4 spaces
  ``
- Line 287: Indentation over 4 spaces
  `from app.models.battle import Battle`
- Line 288: Indentation over 4 spaces
  `battles = Battle.get_cabal_battle_history(cabal_id)`
- Line 289: Indentation over 4 spaces
  ``
- Line 290: Indentation over 4 spaces
  `return render_template('cabal/battles.html', cabal=cabal, battles=battles)`
- Line 295: Indentation over 4 spaces
  `"""Remove a member from the cabal"""`
- Line 296: Indentation over 4 spaces
  `cabal = Cabal.query.get_or_404(cabal_id)`
- Line 297: Indentation over 4 spaces
  ``
- Line 298: Indentation over 4 spaces
  `# Only leader can remove members`
- Line 299: Indentation over 4 spaces
  `if cabal.leader_id != current_user.chad.id:`
- Line 300: Indentation over 4 spaces
  `flash('Only the cabal leader can remove members', 'danger')`
- Line 301: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 302: Indentation over 4 spaces
  ``
- Line 303: Indentation over 4 spaces
  `chad_id = request.args.get('chad_id')`
- Line 304: Indentation over 4 spaces
  `if not chad_id:`
- Line 305: Indentation over 4 spaces
  `flash('Member ID is required', 'danger')`
- Line 306: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 307: Indentation over 4 spaces
  ``
- Line 308: Indentation over 4 spaces
  `# Validate UUID format`
- Line 309: Indentation over 4 spaces
  `if not re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', chad_id, re.I):`
- Line 310: Indentation over 4 spaces
  `flash('Invalid member ID format', 'danger')`
- Line 311: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 312: Indentation over 4 spaces
  ``
- Line 313: Indentation over 4 spaces
  `success, message = cabal.remove_member(chad_id)`
- Line 314: Indentation over 4 spaces
  ``
- Line 315: Indentation over 4 spaces
  `if success:`
- Line 316: Indentation over 4 spaces
  `flash('Member removed successfully', 'success')`
- Line 317: Indentation over 4 spaces
  `else:`
- Line 318: Indentation over 4 spaces
  `flash(message, 'danger')`
- Line 319: Indentation over 4 spaces
  ``
- Line 320: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 325: Indentation over 4 spaces
  `"""Promote a member to cabal leader"""`
- Line 326: Indentation over 4 spaces
  `cabal = Cabal.query.get_or_404(cabal_id)`
- Line 327: Indentation over 4 spaces
  ``
- Line 328: Indentation over 4 spaces
  `# Only current leader can promote`
- Line 329: Indentation over 4 spaces
  `if cabal.leader_id != current_user.chad.id:`
- Line 330: Indentation over 4 spaces
  `flash('Only the cabal leader can promote members', 'danger')`
- Line 331: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 332: Indentation over 4 spaces
  ``
- Line 333: Indentation over 4 spaces
  `chad_id = request.args.get('chad_id')`
- Line 334: Indentation over 4 spaces
  `if not chad_id:`
- Line 335: Indentation over 4 spaces
  `flash('Member ID is required', 'danger')`
- Line 336: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 337: Indentation over 4 spaces
  ``
- Line 338: Indentation over 4 spaces
  `# Validate UUID format`
- Line 339: Indentation over 4 spaces
  `if not re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', chad_id, re.I):`
- Line 340: Indentation over 4 spaces
  `flash('Invalid member ID format', 'danger')`
- Line 341: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 342: Indentation over 4 spaces
  ``
- Line 343: Indentation over 4 spaces
  `success, message = cabal.change_leader(chad_id)`
- Line 344: Indentation over 4 spaces
  ``
- Line 345: Indentation over 4 spaces
  `if success:`
- Line 346: Indentation over 4 spaces
  `flash('Leadership transferred successfully', 'success')`
- Line 347: Indentation over 4 spaces
  `else:`
- Line 348: Indentation over 4 spaces
  `flash(message, 'danger')`
- Line 349: Indentation over 4 spaces
  ``
- Line 350: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 355: Indentation over 4 spaces
  `"""Disband the cabal"""`
- Line 356: Indentation over 4 spaces
  `cabal = Cabal.query.get_or_404(cabal_id)`
- Line 357: Indentation over 4 spaces
  ``
- Line 358: Indentation over 4 spaces
  `# Only leader can disband`
- Line 359: Indentation over 4 spaces
  `if cabal.leader_id != current_user.chad.id:`
- Line 360: Indentation over 4 spaces
  `flash('Only the cabal leader can disband the cabal', 'danger')`
- Line 361: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 362: Indentation over 4 spaces
  ``
- Line 363: Indentation over 4 spaces
  `success, message = cabal.disband()`
- Line 364: Indentation over 4 spaces
  ``
- Line 365: Indentation over 4 spaces
  `if success:`
- Line 366: Indentation over 4 spaces
  `flash('Cabal disbanded successfully', 'success')`
- Line 367: Indentation over 4 spaces
  `else:`
- Line 368: Indentation over 4 spaces
  `flash(message, 'danger')`
- Line 369: Indentation over 4 spaces
  ``
- Line 370: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 375: Indentation over 4 spaces
  `"""Appoint an officer to a specific role"""`
- Line 376: Indentation over 4 spaces
  `cabal = Cabal.query.get_or_404(cabal_id)`
- Line 377: Indentation over 4 spaces
  ``
- Line 378: Indentation over 4 spaces
  `# Only leader can appoint officers`
- Line 379: Indentation over 4 spaces
  `if cabal.leader_id != current_user.chad.id:`
- Line 380: Indentation over 4 spaces
  `flash('Only the Lord of the Shill can appoint officers', 'danger')`
- Line 381: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 382: Indentation over 4 spaces
  ``
- Line 383: Indentation over 4 spaces
  `chad_id = request.form.get('chad_id', '').strip()`
- Line 384: Indentation over 4 spaces
  `role_type = request.form.get('role_type', '').strip()`
- Line 385: Indentation over 4 spaces
  ``
- Line 386: Indentation over 4 spaces
  `# Validate input`
- Line 387: Indentation over 4 spaces
  `if not chad_id or not role_type:`
- Line 388: Indentation over 4 spaces
  `flash('Member ID and role type are required', 'danger')`
- Line 389: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 390: Indentation over 4 spaces
  ``
- Line 391: Indentation over 4 spaces
  `# Validate UUID format for chad_id`
- Line 392: Indentation over 4 spaces
  `if not re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', chad_id, re.I):`
- Line 393: Indentation over 4 spaces
  `flash('Invalid member ID format', 'danger')`
- Line 394: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 395: Indentation over 4 spaces
  ``
- Line 396: Indentation over 4 spaces
  `# Validate role_type`
- Line 397: Indentation over 4 spaces
  `valid_roles = ['clout', 'roast_level', 'cringe_resistance', 'drip_factor']`
- Line 398: Indentation over 4 spaces
  `if role_type not in valid_roles:`
- Line 399: Indentation over 4 spaces
  `flash('Invalid role type', 'danger')`
- Line 400: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 401: Indentation over 4 spaces
  ``
- Line 402: Indentation over 4 spaces
  `success, message = cabal.appoint_officer(chad_id, role_type)`
- Line 403: Indentation over 4 spaces
  ``
- Line 404: Indentation over 4 spaces
  `if success:`
- Line 405: Indentation over 4 spaces
  `flash(message, 'success')`
- Line 406: Indentation over 4 spaces
  `else:`
- Line 407: Indentation over 4 spaces
  `flash(message, 'danger')`
- Line 408: Indentation over 4 spaces
  ``
- Line 409: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 414: Indentation over 4 spaces
  `"""Remove an officer from their role"""`
- Line 415: Indentation over 4 spaces
  `cabal = Cabal.query.get_or_404(cabal_id)`
- Line 416: Indentation over 4 spaces
  ``
- Line 417: Indentation over 4 spaces
  `# Only leader can remove officers`
- Line 418: Indentation over 4 spaces
  `if cabal.leader_id != current_user.chad.id:`
- Line 419: Indentation over 4 spaces
  `flash('Only the Lord of the Shill can remove officers', 'danger')`
- Line 420: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 421: Indentation over 4 spaces
  ``
- Line 422: Indentation over 4 spaces
  `# Validate role_type`
- Line 423: Indentation over 4 spaces
  `valid_roles = ['clout', 'roast_level', 'cringe_resistance', 'drip_factor']`
- Line 424: Indentation over 4 spaces
  `if role_type not in valid_roles:`
- Line 425: Indentation over 4 spaces
  `flash('Invalid role type', 'danger')`
- Line 426: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 427: Indentation over 4 spaces
  ``
- Line 428: Indentation over 4 spaces
  `success, message = cabal.remove_officer(role_type)`
- Line 429: Indentation over 4 spaces
  ``
- Line 430: Indentation over 4 spaces
  `if success:`
- Line 431: Indentation over 4 spaces
  `flash(message, 'success')`
- Line 432: Indentation over 4 spaces
  `else:`
- Line 433: Indentation over 4 spaces
  `flash(message, 'danger')`
- Line 434: Indentation over 4 spaces
  ``
- Line 435: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 440: Indentation over 4 spaces
  `"""Vote to remove the current cabal leader"""`
- Line 441: Indentation over 4 spaces
  `cabal = Cabal.query.get_or_404(cabal_id)`
- Line 442: Indentation over 4 spaces
  ``
- Line 443: Indentation over 4 spaces
  `# Leader can't vote to remove themselves`
- Line 444: Indentation over 4 spaces
  `if cabal.leader_id == current_user.chad.id:`
- Line 445: Indentation over 4 spaces
  `flash('You cannot vote to remove yourself as leader', 'danger')`
- Line 446: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 447: Indentation over 4 spaces
  ``
- Line 448: Indentation over 4 spaces
  `success, message = cabal.vote_to_remove_leader(current_user.chad.id)`
- Line 449: Indentation over 4 spaces
  ``
- Line 450: Indentation over 4 spaces
  `if success:`
- Line 451: Indentation over 4 spaces
  `flash(message, 'success')`
- Line 452: Indentation over 4 spaces
  `else:`
- Line 453: Indentation over 4 spaces
  `flash(message, 'danger')`
- Line 454: Indentation over 4 spaces
  ``
- Line 455: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 460: Indentation over 4 spaces
  `"""Schedule a cabal battle"""`
- Line 461: Indentation over 4 spaces
  `cabal = Cabal.query.get_or_404(cabal_id)`
- Line 462: Indentation over 4 spaces
  ``
- Line 463: Indentation over 4 spaces
  `# Only leader can schedule battles`
- Line 464: Indentation over 4 spaces
  `if cabal.leader_id != current_user.chad.id:`
- Line 465: Indentation over 4 spaces
  `flash('Only the Lord of the Shill can schedule battles', 'danger')`
- Line 466: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 467: Indentation over 4 spaces
  ``
- Line 468: Indentation over 4 spaces
  `if request.method == 'POST':`
- Line 469: Indentation over 4 spaces
  `opponent_cabal_id = request.form.get('opponent_cabal_id', '').strip()`
- Line 470: Indentation over 4 spaces
  `battle_date = request.form.get('battle_date', '').strip()`
- Line 471: Indentation over 4 spaces
  `battle_time = request.form.get('battle_time', '').strip()`
- Line 472: Indentation over 4 spaces
  ``
- Line 473: Indentation over 4 spaces
  `# Validate input`
- Line 474: Indentation over 4 spaces
  `if not opponent_cabal_id or not battle_date or not battle_time:`
- Line 475: Indentation over 4 spaces
  `flash('All fields are required', 'danger')`
- Line 476: Indentation over 4 spaces
  `return redirect(url_for('cabal.schedule_battle', cabal_id=cabal_id))`
- Line 477: Indentation over 4 spaces
  ``
- Line 478: Indentation over 4 spaces
  `# Validate UUID format for opponent_cabal_id`
- Line 479: Indentation over 4 spaces
  `if not re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', opponent_cabal_id, re.I):`
- Line 480: Indentation over 4 spaces
  `flash('Invalid opponent cabal ID format', 'danger')`
- Line 481: Indentation over 4 spaces
  `return redirect(url_for('cabal.schedule_battle', cabal_id=cabal_id))`
- Line 482: Indentation over 4 spaces
  ``
- Line 483: Indentation over 4 spaces
  `# Validate date and time format`
- Line 484: Indentation over 4 spaces
  `date_pattern = r'^\d{4}-\d{2}-\d{2}$'`
- Line 485: Indentation over 4 spaces
  `time_pattern = r'^\d{2}:\d{2}$'`
- Line 486: Indentation over 4 spaces
  ``
- Line 487: Indentation over 4 spaces
  `if not re.match(date_pattern, battle_date):`
- Line 488: Indentation over 4 spaces
  `flash('Invalid date format (YYYY-MM-DD required)', 'danger')`
- Line 489: Indentation over 4 spaces
  `return redirect(url_for('cabal.schedule_battle', cabal_id=cabal_id))`
- Line 490: Indentation over 4 spaces
  ``
- Line 491: Indentation over 4 spaces
  `if not re.match(time_pattern, battle_time):`
- Line 492: Indentation over 4 spaces
  `flash('Invalid time format (HH:MM required)', 'danger')`
- Line 493: Indentation over 4 spaces
  `return redirect(url_for('cabal.schedule_battle', cabal_id=cabal_id))`
- Line 494: Indentation over 4 spaces
  ``
- Line 495: Indentation over 4 spaces
  `# Check if opponent cabal exists`
- Line 496: Indentation over 4 spaces
  `opponent_cabal = Cabal.query.get(opponent_cabal_id)`
- Line 497: Indentation over 4 spaces
  `if not opponent_cabal:`
- Line 498: Indentation over 4 spaces
  `flash('Opponent cabal not found', 'danger')`
- Line 499: Indentation over 4 spaces
  `return redirect(url_for('cabal.schedule_battle', cabal_id=cabal_id))`
- Line 500: Indentation over 4 spaces
  ``
- Line 501: Indentation over 4 spaces
  `# Convert date and time to datetime`
- Line 502: Indentation over 4 spaces
  `try:`
- Line 503: Indentation over 4 spaces
  `scheduled_at = datetime.strptime(f"{battle_date} {battle_time}", "%Y-%m-%d %H:%M")`
- Line 504: Indentation over 4 spaces
  `except ValueError:`
- Line 505: Indentation over 4 spaces
  `flash('Invalid date or time format', 'danger')`
- Line 506: Indentation over 4 spaces
  `return redirect(url_for('cabal.schedule_battle', cabal_id=cabal_id))`
- Line 507: Indentation over 4 spaces
  ``
- Line 508: Indentation over 4 spaces
  `# Check if the scheduled time is in the future`
- Line 509: Indentation over 4 spaces
  `if scheduled_at <= datetime.utcnow():`
- Line 510: Indentation over 4 spaces
  `flash('Battle must be scheduled in the future', 'danger')`
- Line 511: Indentation over 4 spaces
  `return redirect(url_for('cabal.schedule_battle', cabal_id=cabal_id))`
- Line 512: Indentation over 4 spaces
  ``
- Line 513: Indentation over 4 spaces
  `# Schedule the battle`
- Line 514: Indentation over 4 spaces
  `success, message = cabal.schedule_battle(opponent_cabal_id, scheduled_at)`
- Line 515: Indentation over 4 spaces
  ``
- Line 516: Indentation over 4 spaces
  `if success:`
- Line 517: Indentation over 4 spaces
  `flash(message, 'success')`
- Line 518: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 519: Indentation over 4 spaces
  `else:`
- Line 520: Indentation over 4 spaces
  `flash(message, 'danger')`
- Line 521: Indentation over 4 spaces
  `return redirect(url_for('cabal.schedule_battle', cabal_id=cabal_id))`
- Line 522: Indentation over 4 spaces
  ``
- Line 523: Indentation over 4 spaces
  `# Get all other cabals for the opponent selection dropdown`
- Line 524: Indentation over 4 spaces
  `other_cabals = Cabal.query.filter(Cabal.id != cabal_id).all()`
- Line 525: Indentation over 4 spaces
  ``
- Line 526: Indentation over 4 spaces
  `# Get battle count for this week`
- Line 527: Indentation over 4 spaces
  `battles_this_week = CabalBattle.count_battles_this_week(cabal_id)`
- Line 528: Indentation over 4 spaces
  `battles_remaining = 3 - battles_this_week`
- Line 529: Indentation over 4 spaces
  ``
- Line 530: Indentation over 4 spaces
  `# Add current datetime for template`
- Line 531: Indentation over 4 spaces
  `now = datetime.utcnow()`
- Line 532: Indentation over 4 spaces
  ``
- Line 533: Indentation over 4 spaces
  `return render_template('cabal/schedule_battle.html',`
- Line 534: Indentation over 4 spaces
  `cabal=cabal,`
- Line 535: Indentation over 4 spaces
  `other_cabals=other_cabals,`
- Line 536: Indentation over 4 spaces
  `battles_this_week=battles_this_week,`
- Line 537: Indentation over 4 spaces
  `battles_remaining=battles_remaining,`
- Line 538: Indentation over 4 spaces
  `now=now)`
- Line 543: Indentation over 4 spaces
  `"""Opt into participating in a cabal battle"""`
- Line 544: Indentation over 4 spaces
  `battle = CabalBattle.query.get_or_404(battle_id)`
- Line 545: Indentation over 4 spaces
  ``
- Line 546: Indentation over 4 spaces
  `# Check if user is in the cabal`
- Line 547: Indentation over 4 spaces
  `cabal_member = CabalMember.query.filter_by(`
- Line 548: Indentation over 4 spaces
  `chad_id=current_user.chad.id,`
- Line 549: Indentation over 4 spaces
  `cabal_id=battle.cabal_id`
- Line 550: Indentation over 4 spaces
  `).first()`
- Line 551: Indentation over 4 spaces
  ``
- Line 552: Indentation over 4 spaces
  `if not cabal_member:`
- Line 553: Indentation over 4 spaces
  `flash('You are not a member of this cabal', 'danger')`
- Line 554: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 555: Indentation over 4 spaces
  ``
- Line 556: Indentation over 4 spaces
  `# Try to opt in`
- Line 557: Indentation over 4 spaces
  `success, message = cabal_member.opt_into_battle(battle_id)`
- Line 558: Indentation over 4 spaces
  ``
- Line 559: Indentation over 4 spaces
  `if success:`
- Line 560: Indentation over 4 spaces
  `flash(message, 'success')`
- Line 561: Indentation over 4 spaces
  `else:`
- Line 562: Indentation over 4 spaces
  `flash(message, 'danger')`
- Line 563: Indentation over 4 spaces
  ``
- Line 564: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 569: Indentation over 4 spaces
  `"""View all upcoming cabal battles"""`
- Line 570: Indentation over 4 spaces
  `# Get user's cabal`
- Line 571: Indentation over 4 spaces
  `cabal_member = CabalMember.query.filter_by(chad_id=current_user.chad.id).first()`
- Line 572: Indentation over 4 spaces
  ``
- Line 573: Indentation over 4 spaces
  `if not cabal_member:`
- Line 574: Indentation over 4 spaces
  `flash('You are not a member of a cabal', 'danger')`
- Line 575: Indentation over 4 spaces
  `return redirect(url_for('cabal.index'))`
- Line 576: Indentation over 4 spaces
  ``
- Line 577: Indentation over 4 spaces
  `# Get upcoming battles for user's cabal`
- Line 578: Indentation over 4 spaces
  `upcoming_battles = CabalBattle.query.filter_by(`
- Line 579: Indentation over 4 spaces
  `cabal_id=cabal_member.cabal_id,`
- Line 580: Indentation over 4 spaces
  `completed=False`
- Line 581: Indentation over 4 spaces
  `).filter(`
- Line 582: Indentation over 4 spaces
  `CabalBattle.scheduled_at > datetime.utcnow()`
- Line 583: Indentation over 4 spaces
  `).order_by(CabalBattle.scheduled_at).all()`
- Line 584: Indentation over 4 spaces
  ``
- Line 585: Indentation over 4 spaces
  `# Get past battles`
- Line 586: Indentation over 4 spaces
  `past_battles = CabalBattle.query.filter_by(`
- Line 587: Indentation over 4 spaces
  `cabal_id=cabal_member.cabal_id,`
- Line 588: Indentation over 4 spaces
  `completed=True`
- Line 589: Indentation over 4 spaces
  `).order_by(CabalBattle.scheduled_at.desc()).limit(10).all()`
- Line 590: Indentation over 4 spaces
  ``
- Line 591: Indentation over 4 spaces
  `# Check which battles the user has opted into`
- Line 592: Indentation over 4 spaces
  `opted_battles = set()`
- Line 593: Indentation over 4 spaces
  `for battle in upcoming_battles:`
- Line 594: Indentation over 4 spaces
  `participant = CabalBattleParticipant.query.filter_by(`
- Line 595: Indentation over 4 spaces
  `battle_id=battle.id,`
- Line 596: Indentation over 4 spaces
  `chad_id=current_user.chad.id`
- Line 597: Indentation over 4 spaces
  `).first()`
- Line 598: Indentation over 4 spaces
  ``
- Line 599: Indentation over 4 spaces
  `if participant:`
- Line 600: Indentation over 4 spaces
  `opted_battles.add(battle.id)`
- Line 601: Indentation over 4 spaces
  ``
- Line 602: Indentation over 4 spaces
  `# Add current datetime for template`
- Line 603: Indentation over 4 spaces
  `now = datetime.utcnow()`
- Line 604: Indentation over 4 spaces
  ``
- Line 605: Indentation over 4 spaces
  `return render_template('cabal/all_battles.html',`
- Line 606: Indentation over 4 spaces
  `cabal=cabal_member.cabal,`
- Line 607: Indentation over 4 spaces
  `upcoming_battles=upcoming_battles,`
- Line 608: Indentation over 4 spaces
  `past_battles=past_battles,`
- Line 609: Indentation over 4 spaces
  `opted_battles=opted_battles,`
- Line 610: Indentation over 4 spaces
  `now=now)`
- Line 614: Indentation over 4 spaces
  `"""Display the cabal leaderboard"""`
- Line 615: Indentation over 4 spaces
  `# Get top 20 cabals by power`
- Line 616: Indentation over 4 spaces
  `top_cabals = Cabal.get_leaderboard(limit=20)`
- Line 617: Indentation over 4 spaces
  ``
- Line 618: Indentation over 4 spaces
  `# For each cabal, get the leader's name`
- Line 619: Indentation over 4 spaces
  `from app.models.chad import Chad`
- Line 620: Indentation over 4 spaces
  `from app.models.user import User`
- Line 621: Indentation over 4 spaces
  ``
- Line 622: Indentation over 4 spaces
  `cabal_data = []`
- Line 623: Indentation over 4 spaces
  `for cabal in top_cabals:`
- Line 624: Indentation over 4 spaces
  `# Update rank`
- Line 625: Indentation over 4 spaces
  `cabal.update_rank()`
- Line 626: Indentation over 4 spaces
  ``
- Line 627: Indentation over 4 spaces
  `# Get leader`
- Line 628: Indentation over 4 spaces
  `leader_chad = Chad.query.get(cabal.leader_id)`
- Line 629: Indentation over 4 spaces
  `if leader_chad:`
- Line 630: Indentation over 4 spaces
  `leader_user = User.query.filter_by(chad_id=leader_chad.id).first()`
- Line 631: Indentation over 4 spaces
  `leader_name = leader_chad.name`
- Line 632: Indentation over 4 spaces
  `leader_username = leader_user.twitter_handle if leader_user else 'Unknown'`
- Line 633: Indentation over 4 spaces
  `else:`
- Line 634: Indentation over 4 spaces
  `leader_name = 'Unknown'`
- Line 635: Indentation over 4 spaces
  `leader_username = 'Unknown'`
- Line 636: Indentation over 4 spaces
  ``
- Line 637: Indentation over 4 spaces
  `cabal_data.append({`
- Line 638: Indentation over 4 spaces
  `'id': cabal.id,`
- Line 639: Indentation over 4 spaces
  `'name': cabal.name,`
- Line 640: Indentation over 4 spaces
  `'rank': cabal.rank,`
- Line 641: Indentation over 4 spaces
  `'level': cabal.level,`
- Line 642: Indentation over 4 spaces
  `'power': int(cabal.total_power),`
- Line 643: Indentation over 4 spaces
  `'member_count': cabal.member_count,`
- Line 644: Indentation over 4 spaces
  `'leader_name': leader_name,`
- Line 645: Indentation over 4 spaces
  `'leader_username': leader_username,`
- Line 646: Indentation over 4 spaces
  `'battles_won': cabal.battles_won,`
- Line 647: Indentation over 4 spaces
  `'battles_lost': cabal.battles_lost,`
- Line 648: Indentation over 4 spaces
  `'win_rate': round((cabal.battles_won / (cabal.battles_won + cabal.battles_lost) * 100) if (cabal.battles_won + cabal.battles_lost) > 0 else 0, 1)`
- Line 649: Indentation over 4 spaces
  `})`
- Line 650: Indentation over 4 spaces
  ``
- Line 651: Indentation over 4 spaces
  `return render_template('cabal/leaderboard.html', cabals=cabal_data)`

### app\models\cabal.py (655 issues)

#### Code Smells
- Line 185: Explicit commit - check transaction management
  `db.session.commit()`
- Line 206: Explicit commit - check transaction management
  `db.session.commit()`
- Line 229: Explicit commit - check transaction management
  `db.session.commit()`
- Line 268: Explicit commit - check transaction management
  `db.session.commit()`
- Line 279: Explicit commit - check transaction management
  `db.session.commit()`
- Line 310: Explicit commit - check transaction management
  `db.session.commit()`
- Line 342: Explicit commit - check transaction management
  `db.session.commit()`
- Line 359: Explicit commit - check transaction management
  `db.session.commit()`
- Line 389: Explicit commit - check transaction management
  `db.session.commit()`
- Line 428: Explicit commit - check transaction management
  `db.session.commit()`
- Line 483: Explicit commit - check transaction management
  `db.session.commit()`
- Line 503: Explicit commit - check transaction management
  `db.session.commit()`
- Line 523: Explicit commit - check transaction management
  `db.session.commit()`
- Line 555: Explicit commit - check transaction management
  `db.session.commit()`
- Line 562: Explicit commit - check transaction management
  `db.session.commit()`
- Line 569: Explicit commit - check transaction management
  `db.session.commit()`
- Line 601: Explicit commit - check transaction management
  `db.session.commit()`
- Line 613: Explicit commit - check transaction management
  `db.session.commit()`
- Line 388: Datetime usage - check for timezone awareness
  `self.debuff_until = datetime.utcnow() + timedelta(seconds=duration_seconds)`
- Line 398: Datetime usage - check for timezone awareness
  `return datetime.utcnow() < self.debuff_until`

#### Best Practice Violations
- Line 20: Function without docstring
  `def __repr__(self):`
- Line 35: Function without docstring
  `def __repr__(self):`
- Line 57: Function without docstring
  `def __repr__(self):`
- Line 61: Function without docstring
  `def get_current_week_number():`
- Line 67: Function without docstring
  `def count_battles_this_week(cls, cabal_id):`
- Line 86: Function without docstring
  `def __repr__(self):`
- Line 120: Function without docstring
  `def __repr__(self):`
- Line 123: Function without docstring
  `def __init__(self, *args, **kwargs):`
- Line 131: Function without docstring
  `def generate_invite_code(length=6):`
- Line 143: Function without docstring
  `def member_count(self):`
- Line 148: Function without docstring
  `def leader_title(self):`
- Line 152: Function without docstring
  `def get_officer_title(self, role_type):`
- Line 162: Function without docstring
  `def get_officer(self, role_type):`
- Line 166: Function without docstring
  `def add_member(self, chad_id):`
- Line 189: Function without docstring
  `def remove_member(self, chad_id):`
- Line 210: Function without docstring
  `def change_leader(self, new_leader_id):`
- Line 233: Function without docstring
  `def appoint_officer(self, chad_id, role_type):`
- Line 272: Function without docstring
  `def remove_officer(self, role_type):`
- Line 283: Function without docstring
  `def vote_to_remove_leader(self, voter_id):`
- Line 364: Function without docstring
  `def add_xp(self, amount):`
- Line 376: Function without docstring
  `def level_up(self):`
- Line 386: Function without docstring
  `def apply_debuff(self, debuff_type, multiplier=0.9, duration_seconds=86400):`
- Line 393: Function without docstring
  `def has_debuff(self):`
- Line 400: Function without docstring
  `def get_active_members(self):`
- Line 404: Function without docstring
  `def get_active_member_count(self):`
- Line 408: Function without docstring
  `def can_schedule_battle(self):`
- Line 413: Function without docstring
  `def schedule_battle(self, opponent_cabal_id, scheduled_at):`
- Line 432: Function without docstring
  `def calculate_total_power(self):`
- Line 487: Function without docstring
  `def disband(self):`
- Line 508: Function without docstring
  `def get_leaderboard(cls, limit=20):`
- Line 514: Function without docstring
  `def update_rank(self):`
- Line 548: Function without docstring
  `def __repr__(self):`
- Line 551: Function without docstring
  `def mark_active(self):`
- Line 559: Function without docstring
  `def mark_inactive(self):`
- Line 566: Function without docstring
  `def increase_contribution(self, amount):`
- Line 573: Function without docstring
  `def opt_into_battle(self, battle_id):`
- Line 605: Function without docstring
  `def check_daily_battle_reset(self):`
- Line 461: Using len() in comparison - use implicit truthiness
  `if len(active_members) > 0:`
- Line 128: Self assignment in method/constructor
  `self.invite_code = self.generate_invite_code()`
- Line 8: Indentation over 4 spaces
  `"""Officer roles in a cabal"""`
- Line 9: Indentation over 4 spaces
  `id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))`
- Line 10: Indentation over 4 spaces
  `cabal_id = db.Column(db.String(36), db.ForeignKey('cabal.id'), nullable=False)`
- Line 11: Indentation over 4 spaces
  `chad_id = db.Column(db.String(36), db.ForeignKey('chad.id'), nullable=False)`
- Line 12: Indentation over 4 spaces
  ``
- Line 13: Indentation over 4 spaces
  `# Officer role type: 'clout', 'roast_level', 'cringe_resistance', 'drip_factor'`
- Line 14: Indentation over 4 spaces
  `role_type = db.Column(db.String(20), nullable=False)`
- Line 15: Indentation over 4 spaces
  `appointed_at = db.Column(db.DateTime, default=datetime.utcnow)`
- Line 16: Indentation over 4 spaces
  ``
- Line 17: Indentation over 4 spaces
  `# Relationships`
- Line 18: Indentation over 4 spaces
  `cabal = db.relationship('Cabal', back_populates='officers')`
- Line 19: Indentation over 4 spaces
  ``
- Line 20: Indentation over 4 spaces
  `def __repr__(self):`
- Line 21: Indentation over 4 spaces
  `return f'<CabalOfficer {self.chad_id} ({self.role_type}) in {self.cabal_id}>'`
- Line 24: Indentation over 4 spaces
  `"""Votes for cabal leadership changes"""`
- Line 25: Indentation over 4 spaces
  `id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))`
- Line 26: Indentation over 4 spaces
  `cabal_id = db.Column(db.String(36), db.ForeignKey('cabal.id'), nullable=False)`
- Line 27: Indentation over 4 spaces
  `voter_id = db.Column(db.String(36), db.ForeignKey('chad.id'), nullable=False)`
- Line 28: Indentation over 4 spaces
  `vote_type = db.Column(db.String(20), nullable=False)  # 'remove_leader', 'new_leader_nomination'`
- Line 29: Indentation over 4 spaces
  `target_id = db.Column(db.String(36), db.ForeignKey('chad.id'), nullable=False)  # Who the vote affects`
- Line 30: Indentation over 4 spaces
  `created_at = db.Column(db.DateTime, default=datetime.utcnow)`
- Line 31: Indentation over 4 spaces
  ``
- Line 32: Indentation over 4 spaces
  `# Relationships`
- Line 33: Indentation over 4 spaces
  `cabal = db.relationship('Cabal')`
- Line 34: Indentation over 4 spaces
  ``
- Line 35: Indentation over 4 spaces
  `def __repr__(self):`
- Line 36: Indentation over 4 spaces
  `return f'<CabalVote {self.vote_type} from {self.voter_id} in {self.cabal_id}>'`
- Line 39: Indentation over 4 spaces
  `"""Tracks cabal battle schedules and participation"""`
- Line 40: Indentation over 4 spaces
  `id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))`
- Line 41: Indentation over 4 spaces
  `cabal_id = db.Column(db.String(36), db.ForeignKey('cabal.id'), nullable=False)`
- Line 42: Indentation over 4 spaces
  `opponent_cabal_id = db.Column(db.String(36), db.ForeignKey('cabal.id'), nullable=True)`
- Line 43: Indentation over 4 spaces
  `scheduled_at = db.Column(db.DateTime, nullable=False)`
- Line 44: Indentation over 4 spaces
  `completed = db.Column(db.Boolean, default=False)`
- Line 45: Indentation over 4 spaces
  `result = db.Column(db.String(10), nullable=True)  # 'win', 'loss', 'draw'`
- Line 46: Indentation over 4 spaces
  ``
- Line 47: Indentation over 4 spaces
  `# Battle limits tracking`
- Line 48: Indentation over 4 spaces
  `week_number = db.Column(db.Integer, nullable=False)  # Track which week this battle belongs to`
- Line 49: Indentation over 4 spaces
  ``
- Line 50: Indentation over 4 spaces
  `created_at = db.Column(db.DateTime, default=datetime.utcnow)`
- Line 51: Indentation over 4 spaces
  ``
- Line 52: Indentation over 4 spaces
  `# Relationships`
- Line 53: Indentation over 4 spaces
  `cabal = db.relationship('Cabal', foreign_keys=[cabal_id])`
- Line 54: Indentation over 4 spaces
  `opponent_cabal = db.relationship('Cabal', foreign_keys=[opponent_cabal_id])`
- Line 55: Indentation over 4 spaces
  `participants = db.relationship('CabalBattleParticipant', back_populates='battle', cascade='all, delete-orphan')`
- Line 56: Indentation over 4 spaces
  ``
- Line 57: Indentation over 4 spaces
  `def __repr__(self):`
- Line 58: Indentation over 4 spaces
  `return f'<CabalBattle {self.id}: {self.cabal_id} vs {self.opponent_cabal_id}>'`
- Line 59: Indentation over 4 spaces
  ``
- Line 60: Indentation over 4 spaces
  `@staticmethod`
- Line 61: Indentation over 4 spaces
  `def get_current_week_number():`
- Line 62: Indentation over 4 spaces
  `"""Get the current week number for battle limit tracking"""`
- Line 63: Indentation over 4 spaces
  `current_date = datetime.utcnow()`
- Line 64: Indentation over 4 spaces
  `return current_date.isocalendar()[1]`
- Line 65: Indentation over 4 spaces
  ``
- Line 66: Indentation over 4 spaces
  `@classmethod`
- Line 67: Indentation over 4 spaces
  `def count_battles_this_week(cls, cabal_id):`
- Line 68: Indentation over 4 spaces
  `"""Count how many battles this cabal has scheduled/completed this week"""`
- Line 69: Indentation over 4 spaces
  `current_week = cls.get_current_week_number()`
- Line 70: Indentation over 4 spaces
  `return cls.query.filter_by(`
- Line 71: Indentation over 4 spaces
  `cabal_id=cabal_id,`
- Line 72: Indentation over 4 spaces
  `week_number=current_week`
- Line 73: Indentation over 4 spaces
  `).count()`
- Line 76: Indentation over 4 spaces
  `"""Tracks which cabal members are participating in a battle"""`
- Line 77: Indentation over 4 spaces
  `id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))`
- Line 78: Indentation over 4 spaces
  `battle_id = db.Column(db.String(36), db.ForeignKey('cabal_battle.id'), nullable=False)`
- Line 79: Indentation over 4 spaces
  `chad_id = db.Column(db.String(36), db.ForeignKey('chad.id'), nullable=False)`
- Line 80: Indentation over 4 spaces
  `cabal_id = db.Column(db.String(36), db.ForeignKey('cabal.id'), nullable=False)`
- Line 81: Indentation over 4 spaces
  `opt_in_time = db.Column(db.DateTime, default=datetime.utcnow)`
- Line 82: Indentation over 4 spaces
  ``
- Line 83: Indentation over 4 spaces
  `# Relationships`
- Line 84: Indentation over 4 spaces
  `battle = db.relationship('CabalBattle', back_populates='participants')`
- Line 85: Indentation over 4 spaces
  ``
- Line 86: Indentation over 4 spaces
  `def __repr__(self):`
- Line 87: Indentation over 4 spaces
  `return f'<CabalBattleParticipant {self.chad_id} in battle {self.battle_id}>'`
- Line 90: Indentation over 4 spaces
  `"""Cabal model for group gameplay"""`
- Line 91: Indentation over 4 spaces
  `id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))`
- Line 92: Indentation over 4 spaces
  `name = db.Column(db.String(50), unique=True, nullable=False)`
- Line 93: Indentation over 4 spaces
  `description = db.Column(db.Text)`
- Line 94: Indentation over 4 spaces
  `leader_id = db.Column(db.String(36), db.ForeignKey('chad.id'), nullable=False)`
- Line 95: Indentation over 4 spaces
  `invite_code = db.Column(db.String(10), unique=True)`
- Line 96: Indentation over 4 spaces
  ``
- Line 97: Indentation over 4 spaces
  `# Cabal stats`
- Line 98: Indentation over 4 spaces
  `level = db.Column(db.Integer, default=1)`
- Line 99: Indentation over 4 spaces
  `xp = db.Column(db.Integer, default=0)`
- Line 100: Indentation over 4 spaces
  `battles_won = db.Column(db.Integer, default=0)`
- Line 101: Indentation over 4 spaces
  `battles_lost = db.Column(db.Integer, default=0)`
- Line 102: Indentation over 4 spaces
  ``
- Line 103: Indentation over 4 spaces
  `# Leaderboard stats`
- Line 104: Indentation over 4 spaces
  `total_power = db.Column(db.Float, default=0.0)`
- Line 105: Indentation over 4 spaces
  `rank = db.Column(db.Integer)`
- Line 106: Indentation over 4 spaces
  ``
- Line 107: Indentation over 4 spaces
  `# Cabal state`
- Line 108: Indentation over 4 spaces
  `is_active = db.Column(db.Boolean, default=True)`
- Line 109: Indentation over 4 spaces
  `debuff_until = db.Column(db.DateTime)  # If set, cabal has reduced stats until this time`
- Line 110: Indentation over 4 spaces
  ``
- Line 111: Indentation over 4 spaces
  `# Last battle metrics`
- Line 112: Indentation over 4 spaces
  `last_battle_at = db.Column(db.DateTime)`
- Line 113: Indentation over 4 spaces
  ``
- Line 114: Indentation over 4 spaces
  `created_at = db.Column(db.DateTime, default=datetime.utcnow)`
- Line 115: Indentation over 4 spaces
  ``
- Line 116: Indentation over 4 spaces
  `# Relationships`
- Line 117: Indentation over 4 spaces
  `members = db.relationship('CabalMember', backref='cabal', lazy='dynamic')`
- Line 118: Indentation over 4 spaces
  `officers = db.relationship('CabalOfficerRole', back_populates='cabal', lazy='dynamic')`
- Line 119: Indentation over 4 spaces
  ``
- Line 120: Indentation over 4 spaces
  `def __repr__(self):`
- Line 121: Indentation over 4 spaces
  `return f'<Cabal {self.name} (Level {self.level})>'`
- Line 122: Indentation over 4 spaces
  ``
- Line 123: Indentation over 4 spaces
  `def __init__(self, *args, **kwargs):`
- Line 124: Indentation over 4 spaces
  `super(Cabal, self).__init__(*args, **kwargs)`
- Line 125: Indentation over 4 spaces
  ``
- Line 126: Indentation over 4 spaces
  `# Generate a unique invite code`
- Line 127: Indentation over 4 spaces
  `if not self.invite_code:`
- Line 128: Indentation over 4 spaces
  `self.invite_code = self.generate_invite_code()`
- Line 129: Indentation over 4 spaces
  ``
- Line 130: Indentation over 4 spaces
  `@staticmethod`
- Line 131: Indentation over 4 spaces
  `def generate_invite_code(length=6):`
- Line 132: Indentation over 4 spaces
  `"""Generate a random invite code"""`
- Line 133: Indentation over 4 spaces
  `characters = string.ascii_uppercase + string.digits`
- Line 134: Indentation over 4 spaces
  `invite_code = ''.join(random.choice(characters) for _ in range(length))`
- Line 135: Indentation over 4 spaces
  ``
- Line 136: Indentation over 4 spaces
  `# Make sure it's unique`
- Line 137: Indentation over 4 spaces
  `while Cabal.query.filter_by(invite_code=invite_code).first():`
- Line 138: Indentation over 4 spaces
  `invite_code = ''.join(random.choice(characters) for _ in range(length))`
- Line 139: Indentation over 4 spaces
  ``
- Line 140: Indentation over 4 spaces
  `return invite_code`
- Line 141: Indentation over 4 spaces
  ``
- Line 142: Indentation over 4 spaces
  `@property`
- Line 143: Indentation over 4 spaces
  `def member_count(self):`
- Line 144: Indentation over 4 spaces
  `"""Get the count of active members"""`
- Line 145: Indentation over 4 spaces
  `return self.members.filter_by(is_active=True).count()`
- Line 146: Indentation over 4 spaces
  ``
- Line 147: Indentation over 4 spaces
  `@property`
- Line 148: Indentation over 4 spaces
  `def leader_title(self):`
- Line 149: Indentation over 4 spaces
  `"""Get the title for the cabal leader"""`
- Line 150: Indentation over 4 spaces
  `return "Lord of the Shill"`
- Line 151: Indentation over 4 spaces
  ``
- Line 152: Indentation over 4 spaces
  `def get_officer_title(self, role_type):`
- Line 153: Indentation over 4 spaces
  `"""Get the title for an officer based on their role"""`
- Line 154: Indentation over 4 spaces
  `titles = {`
- Line 155: Indentation over 4 spaces
  `'clout': 'Clout Commander',`
- Line 156: Indentation over 4 spaces
  `'roast_level': 'Roast Master',`
- Line 157: Indentation over 4 spaces
  `'cringe_resistance': 'Cringe Shield',`
- Line 158: Indentation over 4 spaces
  `'drip_factor': 'Drip Director'`
- Line 159: Indentation over 4 spaces
  `}`
- Line 160: Indentation over 4 spaces
  `return titles.get(role_type, 'Officer')`
- Line 161: Indentation over 4 spaces
  ``
- Line 162: Indentation over 4 spaces
  `def get_officer(self, role_type):`
- Line 163: Indentation over 4 spaces
  `"""Get the officer with the specified role"""`
- Line 164: Indentation over 4 spaces
  `return self.officers.filter_by(role_type=role_type).first()`
- Line 165: Indentation over 4 spaces
  ``
- Line 166: Indentation over 4 spaces
  `def add_member(self, chad_id):`
- Line 167: Indentation over 4 spaces
  `"""Add a member to the cabal"""`
- Line 168: Indentation over 4 spaces
  `# Check if chad is already in a cabal`
- Line 169: Indentation over 4 spaces
  `existing_membership = CabalMember.query.filter_by(chad_id=chad_id).first()`
- Line 170: Indentation over 4 spaces
  `if existing_membership:`
- Line 171: Indentation over 4 spaces
  `return False, "Player is already in a cabal"`
- Line 172: Indentation over 4 spaces
  ``
- Line 173: Indentation over 4 spaces
  `# Check if the cabal is full (now 69 members max)`
- Line 174: Indentation over 4 spaces
  `if self.member_count >= 69:`
- Line 175: Indentation over 4 spaces
  `return False, "Cabal is full (maximum 69 members)"`
- Line 176: Indentation over 4 spaces
  ``
- Line 177: Indentation over 4 spaces
  `# Create cabal membership`
- Line 178: Indentation over 4 spaces
  `member = CabalMember(`
- Line 179: Indentation over 4 spaces
  `cabal_id=self.id,`
- Line 180: Indentation over 4 spaces
  `chad_id=chad_id,`
- Line 181: Indentation over 4 spaces
  `is_active=True`
- Line 182: Indentation over 4 spaces
  `)`
- Line 183: Indentation over 4 spaces
  ``
- Line 184: Indentation over 4 spaces
  `db.session.add(member)`
- Line 185: Indentation over 4 spaces
  `db.session.commit()`
- Line 186: Indentation over 4 spaces
  ``
- Line 187: Indentation over 4 spaces
  `return True, "Member added to cabal"`
- Line 188: Indentation over 4 spaces
  ``
- Line 189: Indentation over 4 spaces
  `def remove_member(self, chad_id):`
- Line 190: Indentation over 4 spaces
  `"""Remove a member from the cabal"""`
- Line 191: Indentation over 4 spaces
  `member = CabalMember.query.filter_by(cabal_id=self.id, chad_id=chad_id).first()`
- Line 192: Indentation over 4 spaces
  ``
- Line 193: Indentation over 4 spaces
  `if not member:`
- Line 194: Indentation over 4 spaces
  `return False, "Player is not in this cabal"`
- Line 195: Indentation over 4 spaces
  ``
- Line 196: Indentation over 4 spaces
  `# If this is the leader, the operation is not allowed`
- Line 197: Indentation over 4 spaces
  `if chad_id == self.leader_id:`
- Line 198: Indentation over 4 spaces
  `return False, "The cabal leader cannot be removed this way"`
- Line 199: Indentation over 4 spaces
  ``
- Line 200: Indentation over 4 spaces
  `# If this is an officer, remove them from their officer role first`
- Line 201: Indentation over 4 spaces
  `officer = self.officers.filter_by(chad_id=chad_id).first()`
- Line 202: Indentation over 4 spaces
  `if officer:`
- Line 203: Indentation over 4 spaces
  `db.session.delete(officer)`
- Line 204: Indentation over 4 spaces
  ``
- Line 205: Indentation over 4 spaces
  `db.session.delete(member)`
- Line 206: Indentation over 4 spaces
  `db.session.commit()`
- Line 207: Indentation over 4 spaces
  ``
- Line 208: Indentation over 4 spaces
  `return True, "Member removed from cabal"`
- Line 209: Indentation over 4 spaces
  ``
- Line 210: Indentation over 4 spaces
  `def change_leader(self, new_leader_id):`
- Line 211: Indentation over 4 spaces
  `"""Change the cabal leader"""`
- Line 212: Indentation over 4 spaces
  `# Check if the new leader is in the cabal`
- Line 213: Indentation over 4 spaces
  `member = CabalMember.query.filter_by(cabal_id=self.id, chad_id=new_leader_id).first()`
- Line 214: Indentation over 4 spaces
  ``
- Line 215: Indentation over 4 spaces
  `if not member:`
- Line 216: Indentation over 4 spaces
  `return False, "The new leader is not in this cabal"`
- Line 217: Indentation over 4 spaces
  ``
- Line 218: Indentation over 4 spaces
  `# Store old leader for reference`
- Line 219: Indentation over 4 spaces
  `old_leader_id = self.leader_id`
- Line 220: Indentation over 4 spaces
  ``
- Line 221: Indentation over 4 spaces
  `# Update leader`
- Line 222: Indentation over 4 spaces
  `self.leader_id = new_leader_id`
- Line 223: Indentation over 4 spaces
  ``
- Line 224: Indentation over 4 spaces
  `# If the old leader was an officer, remove that role`
- Line 225: Indentation over 4 spaces
  `officer = self.officers.filter_by(chad_id=new_leader_id).first()`
- Line 226: Indentation over 4 spaces
  `if officer:`
- Line 227: Indentation over 4 spaces
  `db.session.delete(officer)`
- Line 228: Indentation over 4 spaces
  ``
- Line 229: Indentation over 4 spaces
  `db.session.commit()`
- Line 230: Indentation over 4 spaces
  ``
- Line 231: Indentation over 4 spaces
  `return True, "Cabal leadership transferred"`
- Line 232: Indentation over 4 spaces
  ``
- Line 233: Indentation over 4 spaces
  `def appoint_officer(self, chad_id, role_type):`
- Line 234: Indentation over 4 spaces
  `"""Appoint a member as an officer"""`
- Line 235: Indentation over 4 spaces
  `# Validate role type`
- Line 236: Indentation over 4 spaces
  `valid_roles = ['clout', 'roast_level', 'cringe_resistance', 'drip_factor']`
- Line 237: Indentation over 4 spaces
  `if role_type not in valid_roles:`
- Line 238: Indentation over 4 spaces
  `return False, f"Invalid role type. Must be one of: {', '.join(valid_roles)}"`
- Line 239: Indentation over 4 spaces
  ``
- Line 240: Indentation over 4 spaces
  `# Check if the member is in the cabal`
- Line 241: Indentation over 4 spaces
  `member = CabalMember.query.filter_by(cabal_id=self.id, chad_id=chad_id).first()`
- Line 242: Indentation over 4 spaces
  `if not member:`
- Line 243: Indentation over 4 spaces
  `return False, "The member is not in this cabal"`
- Line 244: Indentation over 4 spaces
  ``
- Line 245: Indentation over 4 spaces
  `# Check if the member is the leader (cannot be both leader and officer)`
- Line 246: Indentation over 4 spaces
  `if chad_id == self.leader_id:`
- Line 247: Indentation over 4 spaces
  `return False, "The cabal leader cannot also be an officer"`
- Line 248: Indentation over 4 spaces
  ``
- Line 249: Indentation over 4 spaces
  `# Check if this role is already filled`
- Line 250: Indentation over 4 spaces
  `existing_officer = self.get_officer(role_type)`
- Line 251: Indentation over 4 spaces
  `if existing_officer:`
- Line 252: Indentation over 4 spaces
  `# If someone else has this role, remove them first`
- Line 253: Indentation over 4 spaces
  `db.session.delete(existing_officer)`
- Line 254: Indentation over 4 spaces
  ``
- Line 255: Indentation over 4 spaces
  `# Check if this chad is already an officer in another role`
- Line 256: Indentation over 4 spaces
  `existing_role = self.officers.filter_by(chad_id=chad_id).first()`
- Line 257: Indentation over 4 spaces
  `if existing_role:`
- Line 258: Indentation over 4 spaces
  `db.session.delete(existing_role)`
- Line 259: Indentation over 4 spaces
  ``
- Line 260: Indentation over 4 spaces
  `# Create the new officer role`
- Line 261: Indentation over 4 spaces
  `officer = CabalOfficerRole(`
- Line 262: Indentation over 4 spaces
  `cabal_id=self.id,`
- Line 263: Indentation over 4 spaces
  `chad_id=chad_id,`
- Line 264: Indentation over 4 spaces
  `role_type=role_type`
- Line 265: Indentation over 4 spaces
  `)`
- Line 266: Indentation over 4 spaces
  ``
- Line 267: Indentation over 4 spaces
  `db.session.add(officer)`
- Line 268: Indentation over 4 spaces
  `db.session.commit()`
- Line 269: Indentation over 4 spaces
  ``
- Line 270: Indentation over 4 spaces
  `return True, f"Member appointed as {self.get_officer_title(role_type)}"`
- Line 271: Indentation over 4 spaces
  ``
- Line 272: Indentation over 4 spaces
  `def remove_officer(self, role_type):`
- Line 273: Indentation over 4 spaces
  `"""Remove an officer from their role"""`
- Line 274: Indentation over 4 spaces
  `officer = self.get_officer(role_type)`
- Line 275: Indentation over 4 spaces
  `if not officer:`
- Line 276: Indentation over 4 spaces
  `return False, f"No officer assigned to {role_type} role"`
- Line 277: Indentation over 4 spaces
  ``
- Line 278: Indentation over 4 spaces
  `db.session.delete(officer)`
- Line 279: Indentation over 4 spaces
  `db.session.commit()`
- Line 280: Indentation over 4 spaces
  ``
- Line 281: Indentation over 4 spaces
  `return True, f"Officer removed from {role_type} role"`
- Line 282: Indentation over 4 spaces
  ``
- Line 283: Indentation over 4 spaces
  `def vote_to_remove_leader(self, voter_id):`
- Line 284: Indentation over 4 spaces
  `"""Cast a vote to remove the current leader"""`
- Line 285: Indentation over 4 spaces
  `# Check if voter is in the cabal`
- Line 286: Indentation over 4 spaces
  `member = CabalMember.query.filter_by(cabal_id=self.id, chad_id=voter_id).first()`
- Line 287: Indentation over 4 spaces
  `if not member:`
- Line 288: Indentation over 4 spaces
  `return False, "You are not a member of this cabal"`
- Line 289: Indentation over 4 spaces
  ``
- Line 290: Indentation over 4 spaces
  `# Check if voter has already voted`
- Line 291: Indentation over 4 spaces
  `existing_vote = CabalVote.query.filter_by(`
- Line 292: Indentation over 4 spaces
  `cabal_id=self.id,`
- Line 293: Indentation over 4 spaces
  `voter_id=voter_id,`
- Line 294: Indentation over 4 spaces
  `vote_type='remove_leader',`
- Line 295: Indentation over 4 spaces
  `target_id=self.leader_id`
- Line 296: Indentation over 4 spaces
  `).first()`
- Line 297: Indentation over 4 spaces
  ``
- Line 298: Indentation over 4 spaces
  `if existing_vote:`
- Line 299: Indentation over 4 spaces
  `return False, "You have already voted to remove the leader"`
- Line 300: Indentation over 4 spaces
  ``
- Line 301: Indentation over 4 spaces
  `# Create the vote`
- Line 302: Indentation over 4 spaces
  `vote = CabalVote(`
- Line 303: Indentation over 4 spaces
  `cabal_id=self.id,`
- Line 304: Indentation over 4 spaces
  `voter_id=voter_id,`
- Line 305: Indentation over 4 spaces
  `vote_type='remove_leader',`
- Line 306: Indentation over 4 spaces
  `target_id=self.leader_id`
- Line 307: Indentation over 4 spaces
  `)`
- Line 308: Indentation over 4 spaces
  ``
- Line 309: Indentation over 4 spaces
  `db.session.add(vote)`
- Line 310: Indentation over 4 spaces
  `db.session.commit()`
- Line 311: Indentation over 4 spaces
  ``
- Line 312: Indentation over 4 spaces
  `# Check if we have enough votes to remove the leader`
- Line 313: Indentation over 4 spaces
  `# Need 3/4 of officers or 3/4 of active members`
- Line 314: Indentation over 4 spaces
  `total_officers = self.officers.count()`
- Line 315: Indentation over 4 spaces
  `officer_votes = CabalVote.query.filter_by(`
- Line 316: Indentation over 4 spaces
  `cabal_id=self.id,`
- Line 317: Indentation over 4 spaces
  `vote_type='remove_leader',`
- Line 318: Indentation over 4 spaces
  `target_id=self.leader_id`
- Line 319: Indentation over 4 spaces
  `).join(CabalOfficerRole, CabalOfficerRole.chad_id == CabalVote.voter_id).count()`
- Line 320: Indentation over 4 spaces
  ``
- Line 321: Indentation over 4 spaces
  `active_members_count = self.get_active_member_count()`
- Line 322: Indentation over 4 spaces
  `total_votes = CabalVote.query.filter_by(`
- Line 323: Indentation over 4 spaces
  `cabal_id=self.id,`
- Line 324: Indentation over 4 spaces
  `vote_type='remove_leader',`
- Line 325: Indentation over 4 spaces
  `target_id=self.leader_id`
- Line 326: Indentation over 4 spaces
  `).count()`
- Line 327: Indentation over 4 spaces
  ``
- Line 328: Indentation over 4 spaces
  `# Check if we have 3/4 of officer votes`
- Line 329: Indentation over 4 spaces
  `if total_officers > 0 and officer_votes >= (total_officers * 0.75):`
- Line 330: Indentation over 4 spaces
  `# Find the most senior member to make the new leader`
- Line 331: Indentation over 4 spaces
  `oldest_member = self.members.filter(`
- Line 332: Indentation over 4 spaces
  `CabalMember.chad_id != self.leader_id`
- Line 333: Indentation over 4 spaces
  `).order_by(CabalMember.joined_at).first()`
- Line 334: Indentation over 4 spaces
  ``
- Line 335: Indentation over 4 spaces
  `if oldest_member:`
- Line 336: Indentation over 4 spaces
  `self.change_leader(oldest_member.chad_id)`
- Line 337: Indentation over 4 spaces
  `# Clear all removal votes`
- Line 338: Indentation over 4 spaces
  `CabalVote.query.filter_by(`
- Line 339: Indentation over 4 spaces
  `cabal_id=self.id,`
- Line 340: Indentation over 4 spaces
  `vote_type='remove_leader'`
- Line 341: Indentation over 4 spaces
  `).delete()`
- Line 342: Indentation over 4 spaces
  `db.session.commit()`
- Line 343: Indentation over 4 spaces
  `return True, "Leader removed by officer vote. The senior-most member is now the leader."`
- Line 344: Indentation over 4 spaces
  ``
- Line 345: Indentation over 4 spaces
  `# Check if we have 3/4 of active member votes`
- Line 346: Indentation over 4 spaces
  `if active_members_count > 0 and total_votes >= (active_members_count * 0.75):`
- Line 347: Indentation over 4 spaces
  `# Find the most senior member to make the new leader`
- Line 348: Indentation over 4 spaces
  `oldest_member = self.members.filter(`
- Line 349: Indentation over 4 spaces
  `CabalMember.chad_id != self.leader_id`
- Line 350: Indentation over 4 spaces
  `).order_by(CabalMember.joined_at).first()`
- Line 351: Indentation over 4 spaces
  ``
- Line 352: Indentation over 4 spaces
  `if oldest_member:`
- Line 353: Indentation over 4 spaces
  `self.change_leader(oldest_member.chad_id)`
- Line 354: Indentation over 4 spaces
  `# Clear all removal votes`
- Line 355: Indentation over 4 spaces
  `CabalVote.query.filter_by(`
- Line 356: Indentation over 4 spaces
  `cabal_id=self.id,`
- Line 357: Indentation over 4 spaces
  `vote_type='remove_leader'`
- Line 358: Indentation over 4 spaces
  `).delete()`
- Line 359: Indentation over 4 spaces
  `db.session.commit()`
- Line 360: Indentation over 4 spaces
  `return True, "Leader removed by member vote. The senior-most member is now the leader."`
- Line 361: Indentation over 4 spaces
  ``
- Line 362: Indentation over 4 spaces
  `return True, "Your vote to remove the leader has been recorded"`
- Line 363: Indentation over 4 spaces
  ``
- Line 364: Indentation over 4 spaces
  `def add_xp(self, amount):`
- Line 365: Indentation over 4 spaces
  `"""Add XP to the cabal and handle level up"""`
- Line 366: Indentation over 4 spaces
  `self.xp += amount`
- Line 367: Indentation over 4 spaces
  ``
- Line 368: Indentation over 4 spaces
  `# Check for level up`
- Line 369: Indentation over 4 spaces
  `xp_for_level_up = self.level * 1000  # More XP needed than individuals`
- Line 370: Indentation over 4 spaces
  ``
- Line 371: Indentation over 4 spaces
  `if self.xp >= xp_for_level_up:`
- Line 372: Indentation over 4 spaces
  `self.level_up()`
- Line 373: Indentation over 4 spaces
  ``
- Line 374: Indentation over 4 spaces
  `return self.level`
- Line 375: Indentation over 4 spaces
  ``
- Line 376: Indentation over 4 spaces
  `def level_up(self):`
- Line 377: Indentation over 4 spaces
  `"""Handle cabal level up"""`
- Line 378: Indentation over 4 spaces
  `self.level += 1`
- Line 379: Indentation over 4 spaces
  ``
- Line 380: Indentation over 4 spaces
  `# Carry over excess XP`
- Line 381: Indentation over 4 spaces
  `excess_xp = self.xp - (self.level * 1000)`
- Line 382: Indentation over 4 spaces
  `self.xp = excess_xp`
- Line 383: Indentation over 4 spaces
  ``
- Line 384: Indentation over 4 spaces
  `return self.level`
- Line 385: Indentation over 4 spaces
  ``
- Line 386: Indentation over 4 spaces
  `def apply_debuff(self, debuff_type, multiplier=0.9, duration_seconds=86400):`
- Line 387: Indentation over 4 spaces
  `"""Apply a temporary debuff to the cabal"""`
- Line 388: Indentation over 4 spaces
  `self.debuff_until = datetime.utcnow() + timedelta(seconds=duration_seconds)`
- Line 389: Indentation over 4 spaces
  `db.session.commit()`
- Line 390: Indentation over 4 spaces
  ``
- Line 391: Indentation over 4 spaces
  `return True, f"Cabal debuffed for {duration_seconds/3600} hours"`
- Line 392: Indentation over 4 spaces
  ``
- Line 393: Indentation over 4 spaces
  `def has_debuff(self):`
- Line 394: Indentation over 4 spaces
  `"""Check if the cabal currently has an active debuff"""`
- Line 395: Indentation over 4 spaces
  `if not self.debuff_until:`
- Line 396: Indentation over 4 spaces
  `return False`
- Line 397: Indentation over 4 spaces
  ``
- Line 398: Indentation over 4 spaces
  `return datetime.utcnow() < self.debuff_until`
- Line 399: Indentation over 4 spaces
  ``
- Line 400: Indentation over 4 spaces
  `def get_active_members(self):`
- Line 401: Indentation over 4 spaces
  `"""Get all active members of the cabal"""`
- Line 402: Indentation over 4 spaces
  `return self.members.filter_by(is_active=True).all()`
- Line 403: Indentation over 4 spaces
  ``
- Line 404: Indentation over 4 spaces
  `def get_active_member_count(self):`
- Line 405: Indentation over 4 spaces
  `"""Get the count of active members"""`
- Line 406: Indentation over 4 spaces
  `return self.members.filter_by(is_active=True).count()`
- Line 407: Indentation over 4 spaces
  ``
- Line 408: Indentation over 4 spaces
  `def can_schedule_battle(self):`
- Line 409: Indentation over 4 spaces
  `"""Check if the cabal can schedule more battles this week"""`
- Line 410: Indentation over 4 spaces
  `battles_this_week = CabalBattle.count_battles_this_week(self.id)`
- Line 411: Indentation over 4 spaces
  `return battles_this_week < 3  # Maximum 3 battles per week`
- Line 412: Indentation over 4 spaces
  ``
- Line 413: Indentation over 4 spaces
  `def schedule_battle(self, opponent_cabal_id, scheduled_at):`
- Line 414: Indentation over 4 spaces
  `"""Schedule a cabal battle"""`
- Line 415: Indentation over 4 spaces
  `# Check if we can schedule more battles this week`
- Line 416: Indentation over 4 spaces
  `if not self.can_schedule_battle():`
- Line 417: Indentation over 4 spaces
  `return False, "Cabal has already scheduled the maximum 3 battles this week"`
- Line 418: Indentation over 4 spaces
  ``
- Line 419: Indentation over 4 spaces
  `# Create the battle`
- Line 420: Indentation over 4 spaces
  `battle = CabalBattle(`
- Line 421: Indentation over 4 spaces
  `cabal_id=self.id,`
- Line 422: Indentation over 4 spaces
  `opponent_cabal_id=opponent_cabal_id,`
- Line 423: Indentation over 4 spaces
  `scheduled_at=scheduled_at,`
- Line 424: Indentation over 4 spaces
  `week_number=CabalBattle.get_current_week_number()`
- Line 425: Indentation over 4 spaces
  `)`
- Line 426: Indentation over 4 spaces
  ``
- Line 427: Indentation over 4 spaces
  `db.session.add(battle)`
- Line 428: Indentation over 4 spaces
  `db.session.commit()`
- Line 429: Indentation over 4 spaces
  ``
- Line 430: Indentation over 4 spaces
  `return True, "Battle scheduled successfully"`
- Line 431: Indentation over 4 spaces
  ``
- Line 432: Indentation over 4 spaces
  `def calculate_total_power(self):`
- Line 433: Indentation over 4 spaces
  `"""Calculate the total battle power of the cabal for battles"""`
- Line 434: Indentation over 4 spaces
  `from app.models.chad import Chad`
- Line 435: Indentation over 4 spaces
  ``
- Line 436: Indentation over 4 spaces
  `total_power = 0`
- Line 437: Indentation over 4 spaces
  `active_members = self.get_active_members()`
- Line 438: Indentation over 4 spaces
  ``
- Line 439: Indentation over 4 spaces
  `for member in active_members:`
- Line 440: Indentation over 4 spaces
  `chad = Chad.query.get(member.chad_id)`
- Line 441: Indentation over 4 spaces
  `if chad:`
- Line 442: Indentation over 4 spaces
  `# Get chad's total stats`
- Line 443: Indentation over 4 spaces
  `stats = chad.get_total_stats()`
- Line 444: Indentation over 4 spaces
  ``
- Line 445: Indentation over 4 spaces
  `# Calculate a power score based on the chad's stats`
- Line 446: Indentation over 4 spaces
  `chad_power = (`
- Line 447: Indentation over 4 spaces
  `stats['clout'] * 0.5 +`
- Line 448: Indentation over 4 spaces
  `stats['roast_level'] * 1.5 +`
- Line 449: Indentation over 4 spaces
  `stats['cringe_resistance'] * 1.2 +`
- Line 450: Indentation over 4 spaces
  `stats['drip_factor'] * 1.0`
- Line 451: Indentation over 4 spaces
  `)`
- Line 452: Indentation over 4 spaces
  ``
- Line 453: Indentation over 4 spaces
  `# Add the chad's power to the total`
- Line 454: Indentation over 4 spaces
  `total_power += chad_power`
- Line 455: Indentation over 4 spaces
  ``
- Line 456: Indentation over 4 spaces
  `# Apply cabal level bonus (5% per level)`
- Line 457: Indentation over 4 spaces
  `level_bonus = 1 + (self.level * 0.05)`
- Line 458: Indentation over 4 spaces
  `total_power *= level_bonus`
- Line 459: Indentation over 4 spaces
  ``
- Line 460: Indentation over 4 spaces
  `# Apply leader bonus (0.1 to all stats)`
- Line 461: Indentation over 4 spaces
  `if len(active_members) > 0:`
- Line 462: Indentation over 4 spaces
  `total_power += (len(active_members) * 0.4)  # 0.1 per stat, 4 stats`
- Line 463: Indentation over 4 spaces
  ``
- Line 464: Indentation over 4 spaces
  `# Apply officer bonuses`
- Line 465: Indentation over 4 spaces
  `for role_type in ['clout', 'roast_level', 'cringe_resistance', 'drip_factor']:`
- Line 466: Indentation over 4 spaces
  `officer = self.get_officer(role_type)`
- Line 467: Indentation over 4 spaces
  `if officer:`
- Line 468: Indentation over 4 spaces
  `# Get officer's chad`
- Line 469: Indentation over 4 spaces
  `officer_chad = Chad.query.get(officer.chad_id)`
- Line 470: Indentation over 4 spaces
  `if officer_chad:`
- Line 471: Indentation over 4 spaces
  `# Get chad's stats`
- Line 472: Indentation over 4 spaces
  `stats = officer_chad.get_total_stats()`
- Line 473: Indentation over 4 spaces
  `# Add half of the officer's stat as a bonus to all members`
- Line 474: Indentation over 4 spaces
  `bonus = stats[role_type] * 0.5 * len(active_members)`
- Line 475: Indentation over 4 spaces
  `total_power += bonus`
- Line 476: Indentation over 4 spaces
  ``
- Line 477: Indentation over 4 spaces
  `# Apply debuff if active`
- Line 478: Indentation over 4 spaces
  `if self.has_debuff():`
- Line 479: Indentation over 4 spaces
  `total_power *= 0.9  # 10% reduction`
- Line 480: Indentation over 4 spaces
  ``
- Line 481: Indentation over 4 spaces
  `# Store the calculated power for leaderboards`
- Line 482: Indentation over 4 spaces
  `self.total_power = total_power`
- Line 483: Indentation over 4 spaces
  `db.session.commit()`
- Line 484: Indentation over 4 spaces
  ``
- Line 485: Indentation over 4 spaces
  `return total_power`
- Line 486: Indentation over 4 spaces
  ``
- Line 487: Indentation over 4 spaces
  `def disband(self):`
- Line 488: Indentation over 4 spaces
  `"""Disband the cabal and remove all members"""`
- Line 489: Indentation over 4 spaces
  `# Delete all officers`
- Line 490: Indentation over 4 spaces
  `self.officers.delete()`
- Line 491: Indentation over 4 spaces
  ``
- Line 492: Indentation over 4 spaces
  `# Delete all battles`
- Line 493: Indentation over 4 spaces
  `CabalBattle.query.filter_by(cabal_id=self.id).delete()`
- Line 494: Indentation over 4 spaces
  ``
- Line 495: Indentation over 4 spaces
  `# Delete all votes`
- Line 496: Indentation over 4 spaces
  `CabalVote.query.filter_by(cabal_id=self.id).delete()`
- Line 497: Indentation over 4 spaces
  ``
- Line 498: Indentation over 4 spaces
  `# Delete all members`
- Line 499: Indentation over 4 spaces
  `self.members.delete()`
- Line 500: Indentation over 4 spaces
  ``
- Line 501: Indentation over 4 spaces
  `# Delete the cabal`
- Line 502: Indentation over 4 spaces
  `db.session.delete(self)`
- Line 503: Indentation over 4 spaces
  `db.session.commit()`
- Line 504: Indentation over 4 spaces
  ``
- Line 505: Indentation over 4 spaces
  `return True, "Cabal disbanded"`
- Line 506: Indentation over 4 spaces
  ``
- Line 507: Indentation over 4 spaces
  `@classmethod`
- Line 508: Indentation over 4 spaces
  `def get_leaderboard(cls, limit=20):`
- Line 509: Indentation over 4 spaces
  `"""Get the top cabals for the leaderboard"""`
- Line 510: Indentation over 4 spaces
  `return cls.query.filter_by(is_active=True).order_by(`
- Line 511: Indentation over 4 spaces
  `cls.total_power.desc()`
- Line 512: Indentation over 4 spaces
  `).limit(limit).all()`
- Line 513: Indentation over 4 spaces
  ``
- Line 514: Indentation over 4 spaces
  `def update_rank(self):`
- Line 515: Indentation over 4 spaces
  `"""Update the cabal's rank in the leaderboard"""`
- Line 516: Indentation over 4 spaces
  `# Count cabals with more power`
- Line 517: Indentation over 4 spaces
  `rank = Cabal.query.filter(`
- Line 518: Indentation over 4 spaces
  `Cabal.total_power > self.total_power,`
- Line 519: Indentation over 4 spaces
  `Cabal.is_active == True`
- Line 520: Indentation over 4 spaces
  `).count() + 1`
- Line 521: Indentation over 4 spaces
  ``
- Line 522: Indentation over 4 spaces
  `self.rank = rank`
- Line 523: Indentation over 4 spaces
  `db.session.commit()`
- Line 524: Indentation over 4 spaces
  ``
- Line 525: Indentation over 4 spaces
  `return rank`
- Line 528: Indentation over 4 spaces
  `"""Membership in a cabal"""`
- Line 529: Indentation over 4 spaces
  `id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))`
- Line 530: Indentation over 4 spaces
  `cabal_id = db.Column(db.String(36), db.ForeignKey('cabal.id'), nullable=False)`
- Line 531: Indentation over 4 spaces
  `chad_id = db.Column(db.String(36), db.ForeignKey('chad.id'), nullable=False, unique=True)`
- Line 532: Indentation over 4 spaces
  ``
- Line 533: Indentation over 4 spaces
  `# Member status`
- Line 534: Indentation over 4 spaces
  `is_active = db.Column(db.Boolean, default=True)`
- Line 535: Indentation over 4 spaces
  ``
- Line 536: Indentation over 4 spaces
  `# Battle participation`
- Line 537: Indentation over 4 spaces
  `battles_participated = db.Column(db.Integer, default=0)`
- Line 538: Indentation over 4 spaces
  `last_battle_at = db.Column(db.DateTime)`
- Line 539: Indentation over 4 spaces
  `daily_battles = db.Column(db.Integer, default=0)`
- Line 540: Indentation over 4 spaces
  `daily_battles_reset = db.Column(db.DateTime)`
- Line 541: Indentation over 4 spaces
  ``
- Line 542: Indentation over 4 spaces
  `# Stats`
- Line 543: Indentation over 4 spaces
  `contribution_score = db.Column(db.Integer, default=0)  # Based on battles, etc.`
- Line 544: Indentation over 4 spaces
  ``
- Line 545: Indentation over 4 spaces
  `joined_at = db.Column(db.DateTime, default=datetime.utcnow)`
- Line 546: Indentation over 4 spaces
  `last_active_at = db.Column(db.DateTime, default=datetime.utcnow)`
- Line 547: Indentation over 4 spaces
  ``
- Line 548: Indentation over 4 spaces
  `def __repr__(self):`
- Line 549: Indentation over 4 spaces
  `return f'<CabalMember {self.chad_id} in {self.cabal_id}>'`
- Line 550: Indentation over 4 spaces
  ``
- Line 551: Indentation over 4 spaces
  `def mark_active(self):`
- Line 552: Indentation over 4 spaces
  `"""Mark the member as active"""`
- Line 553: Indentation over 4 spaces
  `self.is_active = True`
- Line 554: Indentation over 4 spaces
  `self.last_active_at = datetime.utcnow()`
- Line 555: Indentation over 4 spaces
  `db.session.commit()`
- Line 556: Indentation over 4 spaces
  ``
- Line 557: Indentation over 4 spaces
  `return True, "Member marked as active"`
- Line 558: Indentation over 4 spaces
  ``
- Line 559: Indentation over 4 spaces
  `def mark_inactive(self):`
- Line 560: Indentation over 4 spaces
  `"""Mark the member as inactive"""`
- Line 561: Indentation over 4 spaces
  `self.is_active = False`
- Line 562: Indentation over 4 spaces
  `db.session.commit()`
- Line 563: Indentation over 4 spaces
  ``
- Line 564: Indentation over 4 spaces
  `return True, "Member marked as inactive"`
- Line 565: Indentation over 4 spaces
  ``
- Line 566: Indentation over 4 spaces
  `def increase_contribution(self, amount):`
- Line 567: Indentation over 4 spaces
  `"""Increase member's contribution score"""`
- Line 568: Indentation over 4 spaces
  `self.contribution_score += amount`
- Line 569: Indentation over 4 spaces
  `db.session.commit()`
- Line 570: Indentation over 4 spaces
  ``
- Line 571: Indentation over 4 spaces
  `return self.contribution_score`
- Line 572: Indentation over 4 spaces
  ``
- Line 573: Indentation over 4 spaces
  `def opt_into_battle(self, battle_id):`
- Line 574: Indentation over 4 spaces
  `"""Opt into participating in a cabal battle"""`
- Line 575: Indentation over 4 spaces
  `# Check if already opted in`
- Line 576: Indentation over 4 spaces
  `existing = CabalBattleParticipant.query.filter_by(`
- Line 577: Indentation over 4 spaces
  `battle_id=battle_id,`
- Line 578: Indentation over 4 spaces
  `chad_id=self.chad_id`
- Line 579: Indentation over 4 spaces
  `).first()`
- Line 580: Indentation over 4 spaces
  ``
- Line 581: Indentation over 4 spaces
  `if existing:`
- Line 582: Indentation over 4 spaces
  `return False, "Already opted into this battle"`
- Line 583: Indentation over 4 spaces
  ``
- Line 584: Indentation over 4 spaces
  `# Check daily battle limit`
- Line 585: Indentation over 4 spaces
  `self.check_daily_battle_reset()`
- Line 586: Indentation over 4 spaces
  `if self.daily_battles >= 5:  # Maximum 5 battles per day`
- Line 587: Indentation over 4 spaces
  `return False, "You have reached your daily battle limit"`
- Line 588: Indentation over 4 spaces
  ``
- Line 589: Indentation over 4 spaces
  `# Create participation record`
- Line 590: Indentation over 4 spaces
  `participant = CabalBattleParticipant(`
- Line 591: Indentation over 4 spaces
  `battle_id=battle_id,`
- Line 592: Indentation over 4 spaces
  `chad_id=self.chad_id,`
- Line 593: Indentation over 4 spaces
  `cabal_id=self.cabal_id`
- Line 594: Indentation over 4 spaces
  `)`
- Line 595: Indentation over 4 spaces
  ``
- Line 596: Indentation over 4 spaces
  `# Increment battle counters`
- Line 597: Indentation over 4 spaces
  `self.daily_battles += 1`
- Line 598: Indentation over 4 spaces
  `self.battles_participated += 1`
- Line 599: Indentation over 4 spaces
  ``
- Line 600: Indentation over 4 spaces
  `db.session.add(participant)`
- Line 601: Indentation over 4 spaces
  `db.session.commit()`
- Line 602: Indentation over 4 spaces
  ``
- Line 603: Indentation over 4 spaces
  `return True, "Successfully opted into battle"`
- Line 604: Indentation over 4 spaces
  ``
- Line 605: Indentation over 4 spaces
  `def check_daily_battle_reset(self):`
- Line 606: Indentation over 4 spaces
  `"""Check and reset daily battle counter if needed"""`
- Line 607: Indentation over 4 spaces
  `now = datetime.utcnow()`
- Line 608: Indentation over 4 spaces
  ``
- Line 609: Indentation over 4 spaces
  `# If no reset time or it's past midnight from last reset`
- Line 610: Indentation over 4 spaces
  `if not self.daily_battles_reset or (now - self.daily_battles_reset).days >= 1:`
- Line 611: Indentation over 4 spaces
  `self.daily_battles = 0`
- Line 612: Indentation over 4 spaces
  `self.daily_battles_reset = now`
- Line 613: Indentation over 4 spaces
  `db.session.commit()`

### app\templates\cabal\all_battles.html (258 issues)

#### Best Practice Violations
- Line 7: Indentation over 4 spaces
  `<div class="row">`
- Line 8: Indentation over 4 spaces
  `<div class="col-12">`
- Line 9: Indentation over 4 spaces
  `<h1 class="mb-4">Cabal Battles</h1>`
- Line 10: Indentation over 4 spaces
  ``
- Line 11: Indentation over 4 spaces
  `<div class="row mb-4">`
- Line 12: Indentation over 4 spaces
  `<div class="col-md-6">`
- Line 13: Indentation over 4 spaces
  `<div class="card h-100">`
- Line 14: Indentation over 4 spaces
  `<div class="card-header bg-primary text-white">`
- Line 15: Indentation over 4 spaces
  `<h4 class="mb-0">Your Cabal</h4>`
- Line 16: Indentation over 4 spaces
  `</div>`
- Line 17: Indentation over 4 spaces
  `<div class="card-body">`
- Line 18: Indentation over 4 spaces
  `<h5>{{ cabal.name }} (Level {{ cabal.level }})</h5>`
- Line 19: Indentation over 4 spaces
  `<p>Total Power: <strong>{{ cabal.total_power|int }}</strong></p>`
- Line 20: Indentation over 4 spaces
  `<p>Rank: <strong>#{{ cabal.rank }}</strong></p>`
- Line 21: Indentation over 4 spaces
  `<p>Members: <strong>{{ cabal.member_count }}</strong></p>`
- Line 22: Indentation over 4 spaces
  ``
- Line 23: Indentation over 4 spaces
  `<div class="mt-3">`
- Line 24: Indentation over 4 spaces
  `<a href="{{ url_for('cabal.index') }}" class="btn btn-outline-primary">Back to Cabal Home</a>`
- Line 25: Indentation over 4 spaces
  `</div>`
- Line 26: Indentation over 4 spaces
  `</div>`
- Line 27: Indentation over 4 spaces
  `</div>`
- Line 28: Indentation over 4 spaces
  `</div>`
- Line 29: Indentation over 4 spaces
  ``
- Line 30: Indentation over 4 spaces
  `<div class="col-md-6">`
- Line 31: Indentation over 4 spaces
  `<div class="card h-100">`
- Line 32: Indentation over 4 spaces
  `<div class="card-header bg-info text-white">`
- Line 33: Indentation over 4 spaces
  `<h4 class="mb-0">Battle Stats</h4>`
- Line 34: Indentation over 4 spaces
  `</div>`
- Line 35: Indentation over 4 spaces
  `<div class="card-body">`
- Line 36: Indentation over 4 spaces
  `<div class="row text-center">`
- Line 37: Indentation over 4 spaces
  `<div class="col-4">`
- Line 38: Indentation over 4 spaces
  `<h2 class="mb-0">{{ cabal.battles_won }}</h2>`
- Line 39: Indentation over 4 spaces
  `<p>Wins</p>`
- Line 40: Indentation over 4 spaces
  `</div>`
- Line 41: Indentation over 4 spaces
  `<div class="col-4">`
- Line 42: Indentation over 4 spaces
  `<h2 class="mb-0">{{ cabal.battles_lost }}</h2>`
- Line 43: Indentation over 4 spaces
  `<p>Losses</p>`
- Line 44: Indentation over 4 spaces
  `</div>`
- Line 45: Indentation over 4 spaces
  `<div class="col-4">`
- Line 46: Indentation over 4 spaces
  `<h2 class="mb-0">`
- Line 47: Indentation over 4 spaces
  `{% if (cabal.battles_won + cabal.battles_lost) > 0 %}`
- Line 48: Indentation over 4 spaces
  `{{ (cabal.battles_won / (cabal.battles_won + cabal.battles_lost) * 100)|round(1) }}%`
- Line 49: Indentation over 4 spaces
  `{% else %}`
- Line 50: Indentation over 4 spaces
  `0%`
- Line 51: Indentation over 4 spaces
  `{% endif %}`
- Line 52: Indentation over 4 spaces
  `</h2>`
- Line 53: Indentation over 4 spaces
  `<p>Win Rate</p>`
- Line 54: Indentation over 4 spaces
  `</div>`
- Line 55: Indentation over 4 spaces
  `</div>`
- Line 56: Indentation over 4 spaces
  `</div>`
- Line 57: Indentation over 4 spaces
  `</div>`
- Line 58: Indentation over 4 spaces
  `</div>`
- Line 59: Indentation over 4 spaces
  `</div>`
- Line 60: Indentation over 4 spaces
  ``
- Line 61: Indentation over 4 spaces
  `<!-- Upcoming Battles -->`
- Line 62: Indentation over 4 spaces
  `<div class="card mb-4">`
- Line 63: Indentation over 4 spaces
  `<div class="card-header bg-danger text-white">`
- Line 64: Indentation over 4 spaces
  `<h3 class="mb-0">Upcoming Battles</h3>`
- Line 65: Indentation over 4 spaces
  `</div>`
- Line 66: Indentation over 4 spaces
  `<div class="card-body">`
- Line 67: Indentation over 4 spaces
  `{% if upcoming_battles %}`
- Line 68: Indentation over 4 spaces
  `<div class="table-responsive">`
- Line 69: Indentation over 4 spaces
  `<table class="table table-striped">`
- Line 70: Indentation over 4 spaces
  `<thead>`
- Line 71: Indentation over 4 spaces
  `<tr>`
- Line 72: Indentation over 4 spaces
  `<th>Opponent</th>`
- Line 73: Indentation over 4 spaces
  `<th>Scheduled</th>`
- Line 74: Indentation over 4 spaces
  `<th>Time Until Battle</th>`
- Line 75: Indentation over 4 spaces
  `<th>Participants</th>`
- Line 76: Indentation over 4 spaces
  `<th>Actions</th>`
- Line 77: Indentation over 4 spaces
  `</tr>`
- Line 78: Indentation over 4 spaces
  `</thead>`
- Line 79: Indentation over 4 spaces
  `<tbody>`
- Line 80: Indentation over 4 spaces
  `{% for battle in upcoming_battles %}`
- Line 81: Indentation over 4 spaces
  `<tr>`
- Line 82: Indentation over 4 spaces
  `<td>`
- Line 83: Indentation over 4 spaces
  `<strong>{{ battle.opponent_cabal.name }}</strong>`
- Line 84: Indentation over 4 spaces
  `<div class="small text-muted">Power: {{ battle.opponent_cabal.total_power|int }}</div>`
- Line 85: Indentation over 4 spaces
  `</td>`
- Line 86: Indentation over 4 spaces
  `<td>{{ battle.scheduled_at.strftime('%Y-%m-%d %H:%M UTC') }}</td>`
- Line 87: Indentation over 4 spaces
  `<td>`
- Line 88: Indentation over 4 spaces
  `{% set time_diff = (battle.scheduled_at - now).total_seconds() %}`
- Line 89: Indentation over 4 spaces
  `{% if time_diff < 3600 %}`
- Line 90: Indentation over 4 spaces
  `<span class="text-danger">{{ (time_diff / 60)|int }} minutes</span>`
- Line 91: Indentation over 4 spaces
  `{% elif time_diff < 86400 %}`
- Line 92: Indentation over 4 spaces
  `<span class="text-warning">{{ (time_diff / 3600)|int }} hours</span>`
- Line 93: Indentation over 4 spaces
  `{% else %}`
- Line 94: Indentation over 4 spaces
  `<span class="text-info">{{ (time_diff / 86400)|int }} days</span>`
- Line 95: Indentation over 4 spaces
  `{% endif %}`
- Line 96: Indentation over 4 spaces
  `</td>`
- Line 97: Indentation over 4 spaces
  `<td>`
- Line 98: Indentation over 4 spaces
  `<div class="d-flex align-items-center">`
- Line 99: Indentation over 4 spaces
  `<span class="me-2">{{ battle.participant_count }}</span>`
- Line 100: Indentation over 4 spaces
  `<div class="progress flex-grow-1" style="height: 10px;">`
- Line 101: Indentation over 4 spaces
  `<div class="progress-bar bg-success" role="progressbar"`
- Line 102: Indentation over 4 spaces
  `data-width="{{ (battle.participant_count / cabal.member_count * 100)|int }}"`
- Line 103: Indentation over 4 spaces
  `aria-valuenow="{{ battle.participant_count }}"`
- Line 104: Indentation over 4 spaces
  `aria-valuemin="0"`
- Line 105: Indentation over 4 spaces
  `aria-valuemax="{{ cabal.member_count }}">`
- Line 106: Indentation over 4 spaces
  `</div>`
- Line 107: Indentation over 4 spaces
  `</div>`
- Line 108: Indentation over 4 spaces
  `</div>`
- Line 109: Indentation over 4 spaces
  `</td>`
- Line 110: Indentation over 4 spaces
  `<td>`
- Line 111: Indentation over 4 spaces
  `{% if battle.id in opted_battles %}`
- Line 112: Indentation over 4 spaces
  `<span class="badge bg-success">You're In</span>`
- Line 113: Indentation over 4 spaces
  `{% else %}`
- Line 114: Indentation over 4 spaces
  `<a href="{{ url_for('cabal.opt_into_battle', battle_id=battle.id) }}"`
- Line 115: Indentation over 4 spaces
  `class="btn btn-sm btn-outline-success">Opt In</a>`
- Line 116: Indentation over 4 spaces
  `{% endif %}`
- Line 117: Indentation over 4 spaces
  `</td>`
- Line 118: Indentation over 4 spaces
  `</tr>`
- Line 119: Indentation over 4 spaces
  `{% endfor %}`
- Line 120: Indentation over 4 spaces
  `</tbody>`
- Line 121: Indentation over 4 spaces
  `</table>`
- Line 122: Indentation over 4 spaces
  `</div>`
- Line 123: Indentation over 4 spaces
  `{% else %}`
- Line 124: Indentation over 4 spaces
  `<div class="alert alert-info">`
- Line 125: Indentation over 4 spaces
  `<i class="fas fa-info-circle me-2"></i> No upcoming battles scheduled.`
- Line 126: Indentation over 4 spaces
  `</div>`
- Line 127: Indentation over 4 spaces
  `{% endif %}`
- Line 128: Indentation over 4 spaces
  `</div>`
- Line 129: Indentation over 4 spaces
  `</div>`
- Line 130: Indentation over 4 spaces
  ``
- Line 131: Indentation over 4 spaces
  `<!-- Past Battles -->`
- Line 132: Indentation over 4 spaces
  `<div class="card mb-4">`
- Line 133: Indentation over 4 spaces
  `<div class="card-header bg-secondary text-white">`
- Line 134: Indentation over 4 spaces
  `<h3 class="mb-0">Past Battles</h3>`
- Line 135: Indentation over 4 spaces
  `</div>`
- Line 136: Indentation over 4 spaces
  `<div class="card-body">`
- Line 137: Indentation over 4 spaces
  `{% if past_battles %}`
- Line 138: Indentation over 4 spaces
  `<div class="table-responsive">`
- Line 139: Indentation over 4 spaces
  `<table class="table table-striped">`
- Line 140: Indentation over 4 spaces
  `<thead>`
- Line 141: Indentation over 4 spaces
  `<tr>`
- Line 142: Indentation over 4 spaces
  `<th>Opponent</th>`
- Line 143: Indentation over 4 spaces
  `<th>Date</th>`
- Line 144: Indentation over 4 spaces
  `<th>Result</th>`
- Line 145: Indentation over 4 spaces
  `<th>Participants</th>`
- Line 146: Indentation over 4 spaces
  `<th>XP Earned</th>`
- Line 147: Indentation over 4 spaces
  `</tr>`
- Line 148: Indentation over 4 spaces
  `</thead>`
- Line 149: Indentation over 4 spaces
  `<tbody>`
- Line 150: Indentation over 4 spaces
  `{% for battle in past_battles %}`
- Line 151: Indentation over 4 spaces
  `<tr>`
- Line 152: Indentation over 4 spaces
  `<td>`
- Line 153: Indentation over 4 spaces
  `<strong>{{ battle.opponent_cabal.name }}</strong>`
- Line 154: Indentation over 4 spaces
  `</td>`
- Line 155: Indentation over 4 spaces
  `<td>{{ battle.scheduled_at.strftime('%Y-%m-%d %H:%M UTC') }}</td>`
- Line 156: Indentation over 4 spaces
  `<td>`
- Line 157: Indentation over 4 spaces
  `{% if battle.winner_id == cabal.id %}`
- Line 158: Indentation over 4 spaces
  `<span class="badge bg-success">Victory</span>`
- Line 159: Indentation over 4 spaces
  `{% else %}`
- Line 160: Indentation over 4 spaces
  `<span class="badge bg-danger">Defeat</span>`
- Line 161: Indentation over 4 spaces
  `{% endif %}`
- Line 162: Indentation over 4 spaces
  `</td>`
- Line 163: Indentation over 4 spaces
  `<td>{{ battle.participant_count }} members</td>`
- Line 164: Indentation over 4 spaces
  `<td>`
- Line 165: Indentation over 4 spaces
  `{% if battle.xp_earned %}`
- Line 166: Indentation over 4 spaces
  `+{{ battle.xp_earned }} XP`
- Line 167: Indentation over 4 spaces
  `{% else %}`
- Line 168: Indentation over 4 spaces
  `--`
- Line 169: Indentation over 4 spaces
  `{% endif %}`
- Line 170: Indentation over 4 spaces
  `</td>`
- Line 171: Indentation over 4 spaces
  `</tr>`
- Line 172: Indentation over 4 spaces
  `{% endfor %}`
- Line 173: Indentation over 4 spaces
  `</tbody>`
- Line 174: Indentation over 4 spaces
  `</table>`
- Line 175: Indentation over 4 spaces
  `</div>`
- Line 176: Indentation over 4 spaces
  `{% else %}`
- Line 177: Indentation over 4 spaces
  `<div class="alert alert-info">`
- Line 178: Indentation over 4 spaces
  `<i class="fas fa-info-circle me-2"></i> No past battles recorded yet.`
- Line 179: Indentation over 4 spaces
  `</div>`
- Line 180: Indentation over 4 spaces
  `{% endif %}`
- Line 181: Indentation over 4 spaces
  `</div>`
- Line 182: Indentation over 4 spaces
  `</div>`
- Line 183: Indentation over 4 spaces
  ``
- Line 184: Indentation over 4 spaces
  `<!-- Battle Mechanics Info -->`
- Line 185: Indentation over 4 spaces
  `<div class="card mb-4">`
- Line 186: Indentation over 4 spaces
  `<div class="card-header bg-dark text-white">`
- Line 187: Indentation over 4 spaces
  `<h3 class="mb-0">Battle Mechanics</h3>`
- Line 188: Indentation over 4 spaces
  `</div>`
- Line 189: Indentation over 4 spaces
  `<div class="card-body">`
- Line 190: Indentation over 4 spaces
  `<div class="row">`
- Line 191: Indentation over 4 spaces
  `<div class="col-md-6">`
- Line 192: Indentation over 4 spaces
  `<h4>How Battles Work</h4>`
- Line 193: Indentation over 4 spaces
  `<ol>`
- Line 194: Indentation over 4 spaces
  `<li>Battles occur at the scheduled time</li>`
- Line 195: Indentation over 4 spaces
  `<li>Only members who opted in will participate</li>`
- Line 196: Indentation over 4 spaces
  `<li>Cabal power is calculated based on:`
- Line 197: Indentation over 4 spaces
  `<ul>`
- Line 198: Indentation over 4 spaces
  `<li>Participating members' stats</li>`
- Line 199: Indentation over 4 spaces
  `<li>Officer bonuses</li>`
- Line 200: Indentation over 4 spaces
  `<li>Cabal level</li>`
- Line 201: Indentation over 4 spaces
  `</ul>`
- Line 202: Indentation over 4 spaces
  `</li>`
- Line 203: Indentation over 4 spaces
  `<li>Higher participation rate increases chance of victory</li>`
- Line 204: Indentation over 4 spaces
  `<li>Results are determined by combined power and a bit of RNG</li>`
- Line 205: Indentation over 4 spaces
  `</ol>`
- Line 206: Indentation over 4 spaces
  `</div>`
- Line 207: Indentation over 4 spaces
  `<div class="col-md-6">`
- Line 208: Indentation over 4 spaces
  `<h4>Battle Rewards</h4>`
- Line 209: Indentation over 4 spaces
  `<ul>`
- Line 210: Indentation over 4 spaces
  `<li><strong>Victory:</strong>`
- Line 211: Indentation over 4 spaces
  `<ul>`
- Line 212: Indentation over 4 spaces
  `<li>XP for all participating members</li>`
- Line 213: Indentation over 4 spaces
  `<li>Bonus cabal XP</li>`
- Line 214: Indentation over 4 spaces
  `<li>Increased reputation</li>`
- Line 215: Indentation over 4 spaces
  `<li>Special drops based on Drip bonus</li>`
- Line 216: Indentation over 4 spaces
  `</ul>`
- Line 217: Indentation over 4 spaces
  `</li>`
- Line 218: Indentation over 4 spaces
  `<li><strong>Defeat:</strong>`
- Line 219: Indentation over 4 spaces
  `<ul>`
- Line 220: Indentation over 4 spaces
  `<li>Small amount of XP for participation</li>`
- Line 221: Indentation over 4 spaces
  `<li>Valuable battle experience</li>`
- Line 222: Indentation over 4 spaces
  `</ul>`
- Line 223: Indentation over 4 spaces
  `</li>`
- Line 224: Indentation over 4 spaces
  `</ul>`
- Line 225: Indentation over 4 spaces
  `</div>`
- Line 226: Indentation over 4 spaces
  `</div>`
- Line 227: Indentation over 4 spaces
  `</div>`
- Line 228: Indentation over 4 spaces
  `</div>`
- Line 229: Indentation over 4 spaces
  `</div>`
- Line 230: Indentation over 4 spaces
  `</div>`
- Line 236: Indentation over 4 spaces
  `// Add current datetime to template for battle countdown calculations`
- Line 237: Indentation over 4 spaces
  `document.addEventListener('DOMContentLoaded', function() {`
- Line 238: Indentation over 4 spaces
  `// Set width of progress bars based on data-width attribute`
- Line 239: Indentation over 4 spaces
  `const progressBars = document.querySelectorAll('.progress-bar[data-width]');`
- Line 240: Indentation over 4 spaces
  `progressBars.forEach(bar => {`
- Line 241: Indentation over 4 spaces
  `const width = bar.getAttribute('data-width');`
- Line 242: Indentation over 4 spaces
  `bar.style.width = width + '%';`
- Line 243: Indentation over 4 spaces
  `});`
- Line 244: Indentation over 4 spaces
  `});`
- Line 250: Indentation over 4 spaces
  `.progress {`
- Line 251: Indentation over 4 spaces
  `background-color: #343a40;`
- Line 252: Indentation over 4 spaces
  `}`
- Line 253: Indentation over 4 spaces
  ``
- Line 254: Indentation over 4 spaces
  `.progress-bar {`
- Line 255: Indentation over 4 spaces
  `transition: width 0.3s ease;`
- Line 256: Indentation over 4 spaces
  `}`
- Line 257: Indentation over 4 spaces
  ``
- Line 258: Indentation over 4 spaces
  `.btn-pixel {`
- Line 259: Indentation over 4 spaces
  `background-color: #6c5ce7;`
- Line 260: Indentation over 4 spaces
  `color: white;`
- Line 261: Indentation over 4 spaces
  `border: none;`
- Line 262: Indentation over 4 spaces
  `padding: 0.375rem 0.75rem;`
- Line 263: Indentation over 4 spaces
  `border-radius: 0.25rem;`
- Line 264: Indentation over 4 spaces
  `}`
- Line 265: Indentation over 4 spaces
  ``
- Line 266: Indentation over 4 spaces
  `.btn-pixel:hover {`
- Line 267: Indentation over 4 spaces
  `background-color: #5b4cc3;`
- Line 268: Indentation over 4 spaces
  `color: white;`
- Line 269: Indentation over 4 spaces
  `}`
- Line 270: Indentation over 4 spaces
  ``
- Line 271: Indentation over 4 spaces
  `.pixel-font {`
- Line 272: Indentation over 4 spaces
  `font-weight: bold;`
- Line 273: Indentation over 4 spaces
  `letter-spacing: 0.5px;`
- Line 274: Indentation over 4 spaces
  `}`

### app\templates\cabal\battles.html (121 issues)

#### Best Practice Violations
- Line 7: Indentation over 4 spaces
  `<div class="col-12 mb-4">`
- Line 8: Indentation over 4 spaces
  `<a href="{{ url_for('cabal.index') }}" class="btn btn-outline-secondary mb-3">`
- Line 9: Indentation over 4 spaces
  `<i class="fas fa-arrow-left"></i> Back to Cabal`
- Line 10: Indentation over 4 spaces
  `</a>`
- Line 11: Indentation over 4 spaces
  `<h1 class="pixel-font">{{ cabal.name }} - Battle History</h1>`
- Line 12: Indentation over 4 spaces
  `<p>View your cabal's battle history and performance.</p>`
- Line 13: Indentation over 4 spaces
  `</div>`
- Line 17: Indentation over 4 spaces
  `<div class="col-md-12">`
- Line 18: Indentation over 4 spaces
  `<div class="card">`
- Line 19: Indentation over 4 spaces
  `<div class="card-header">Battle Stats</div>`
- Line 20: Indentation over 4 spaces
  `<div class="card-body">`
- Line 21: Indentation over 4 spaces
  `<div class="row">`
- Line 22: Indentation over 4 spaces
  `<div class="col-md-4 text-center">`
- Line 23: Indentation over 4 spaces
  `<h4 class="pixel-font">{{ cabal.battles_won + cabal.battles_lost }}</h4>`
- Line 24: Indentation over 4 spaces
  `<p>Total Battles</p>`
- Line 25: Indentation over 4 spaces
  `</div>`
- Line 26: Indentation over 4 spaces
  `<div class="col-md-4 text-center">`
- Line 27: Indentation over 4 spaces
  `<h4 class="pixel-font text-success">{{ cabal.battles_won }}</h4>`
- Line 28: Indentation over 4 spaces
  `<p>Victories</p>`
- Line 29: Indentation over 4 spaces
  `</div>`
- Line 30: Indentation over 4 spaces
  `<div class="col-md-4 text-center">`
- Line 31: Indentation over 4 spaces
  `<h4 class="pixel-font text-danger">{{ cabal.battles_lost }}</h4>`
- Line 32: Indentation over 4 spaces
  `<p>Defeats</p>`
- Line 33: Indentation over 4 spaces
  `</div>`
- Line 34: Indentation over 4 spaces
  `</div>`
- Line 36: Indentation over 4 spaces
  `<div class="mt-3">`
- Line 37: Indentation over 4 spaces
  `<div class="progress" style="height: 30px;">`
- Line 38: Indentation over 4 spaces
  `{% if cabal.battles_won + cabal.battles_lost > 0 %}`
- Line 39: Indentation over 4 spaces
  `{% set win_percentage = (cabal.battles_won / (cabal.battles_won + cabal.battles_lost)) * 100 %}`
- Line 40: Indentation over 4 spaces
  `<div class="progress-bar bg-success" role="progressbar" data-width="{{ win_percentage }}" aria-valuenow="{{ win_percentage }}" aria-valuemin="0" aria-valuemax="100">`
- Line 41: Indentation over 4 spaces
  `{{ win_percentage | round(1) }}% Win Rate`
- Line 42: Indentation over 4 spaces
  `</div>`
- Line 43: Indentation over 4 spaces
  `{% else %}`
- Line 44: Indentation over 4 spaces
  `<div class="progress-bar" role="progressbar" data-width="0" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100">`
- Line 45: Indentation over 4 spaces
  `No battles yet`
- Line 46: Indentation over 4 spaces
  `</div>`
- Line 47: Indentation over 4 spaces
  `{% endif %}`
- Line 48: Indentation over 4 spaces
  `</div>`
- Line 49: Indentation over 4 spaces
  `</div>`
- Line 50: Indentation over 4 spaces
  `</div>`
- Line 51: Indentation over 4 spaces
  `</div>`
- Line 52: Indentation over 4 spaces
  `</div>`
- Line 57: Indentation over 4 spaces
  `<div class="col-md-12">`
- Line 58: Indentation over 4 spaces
  `<div class="card">`
- Line 59: Indentation over 4 spaces
  `<div class="card-header">Battle History</div>`
- Line 60: Indentation over 4 spaces
  `<div class="card-body">`
- Line 61: Indentation over 4 spaces
  `<div class="table-responsive">`
- Line 62: Indentation over 4 spaces
  `<table class="table table-dark table-hover">`
- Line 63: Indentation over 4 spaces
  `<thead>`
- Line 64: Indentation over 4 spaces
  `<tr>`
- Line 65: Indentation over 4 spaces
  `<th>Date</th>`
- Line 66: Indentation over 4 spaces
  `<th>Opponent</th>`
- Line 67: Indentation over 4 spaces
  `<th>Result</th>`
- Line 68: Indentation over 4 spaces
  `<th>Rewards</th>`
- Line 69: Indentation over 4 spaces
  `<th>Details</th>`
- Line 70: Indentation over 4 spaces
  `</tr>`
- Line 71: Indentation over 4 spaces
  `</thead>`
- Line 72: Indentation over 4 spaces
  `<tbody>`
- Line 73: Indentation over 4 spaces
  `{% for battle in battles %}`
- Line 74: Indentation over 4 spaces
  `<tr>`
- Line 75: Indentation over 4 spaces
  `<td>{{ battle.completed_at.strftime('%Y-%m-%d %H:%M') if battle.completed_at else battle.created_at.strftime('%Y-%m-%d %H:%M') }}</td>`
- Line 76: Indentation over 4 spaces
  `<td>`
- Line 77: Indentation over 4 spaces
  `{% if battle.initiator_cabal_id == cabal.id %}`
- Line 78: Indentation over 4 spaces
  `{{ battle.opponent_cabal.name if battle.opponent_cabal else 'Unknown' }}`
- Line 79: Indentation over 4 spaces
  `{% else %}`
- Line 80: Indentation over 4 spaces
  `{{ battle.initiator_cabal.name if battle.initiator_cabal else 'Unknown' }}`
- Line 81: Indentation over 4 spaces
  `{% endif %}`
- Line 82: Indentation over 4 spaces
  `</td>`
- Line 83: Indentation over 4 spaces
  `<td>`
- Line 84: Indentation over 4 spaces
  `{% if battle.status == 'completed' %}`
- Line 85: Indentation over 4 spaces
  `{% if battle.is_draw %}`
- Line 86: Indentation over 4 spaces
  `<span class="badge bg-warning">Draw</span>`
- Line 87: Indentation over 4 spaces
  `{% elif battle.winner_id and ((battle.initiator_cabal_id == cabal.id and battle.battle_data.result == 'initiator_win') or (battle.opponent_cabal_id == cabal.id and battle.battle_data.result == 'opponent_win')) %}`
- Line 88: Indentation over 4 spaces
  `<span class="badge bg-success">Victory</span>`
- Line 89: Indentation over 4 spaces
  `{% else %}`
- Line 90: Indentation over 4 spaces
  `<span class="badge bg-danger">Defeat</span>`
- Line 91: Indentation over 4 spaces
  `{% endif %}`
- Line 92: Indentation over 4 spaces
  `{% else %}`
- Line 93: Indentation over 4 spaces
  `<span class="badge bg-secondary">{{ battle.status }}</span>`
- Line 94: Indentation over 4 spaces
  `{% endif %}`
- Line 95: Indentation over 4 spaces
  `</td>`
- Line 96: Indentation over 4 spaces
  `<td>`
- Line 97: Indentation over 4 spaces
  `{% if battle.status == 'completed' and battle.winner_id and ((battle.initiator_cabal_id == cabal.id and battle.battle_data.result == 'initiator_win') or (battle.opponent_cabal_id == cabal.id and battle.battle_data.result == 'opponent_win')) %}`
- Line 98: Indentation over 4 spaces
  `<span class="text-success">+{{ battle.coin_reward }} coins</span><br>`
- Line 99: Indentation over 4 spaces
  `<small>+{{ battle.xp_reward }} XP</small>`
- Line 100: Indentation over 4 spaces
  `{% else %}`
- Line 101: Indentation over 4 spaces
  `-`
- Line 102: Indentation over 4 spaces
  `{% endif %}`
- Line 103: Indentation over 4 spaces
  `</td>`
- Line 104: Indentation over 4 spaces
  `<td>`
- Line 105: Indentation over 4 spaces
  `<a href="{{ url_for('battle.view', battle_id=battle.id) }}" class="btn btn-sm btn-pixel">View</a>`
- Line 106: Indentation over 4 spaces
  `</td>`
- Line 107: Indentation over 4 spaces
  `</tr>`
- Line 108: Indentation over 4 spaces
  `{% endfor %}`
- Line 109: Indentation over 4 spaces
  `</tbody>`
- Line 110: Indentation over 4 spaces
  `</table>`
- Line 111: Indentation over 4 spaces
  `</div>`
- Line 112: Indentation over 4 spaces
  `</div>`
- Line 113: Indentation over 4 spaces
  `</div>`
- Line 114: Indentation over 4 spaces
  `</div>`
- Line 118: Indentation over 4 spaces
  `<div class="col-md-12">`
- Line 119: Indentation over 4 spaces
  `<div class="alert alert-info">`
- Line 120: Indentation over 4 spaces
  `<p>Your cabal hasn't participated in any battles yet.</p>`
- Line 121: Indentation over 4 spaces
  `<a href="{{ url_for('battle.cabal_battle') }}" class="btn btn-pixel mt-2">Find a Cabal Battle</a>`
- Line 122: Indentation over 4 spaces
  `</div>`
- Line 123: Indentation over 4 spaces
  `</div>`
- Line 131: Indentation over 4 spaces
  `document.addEventListener('DOMContentLoaded', function() {`
- Line 132: Indentation over 4 spaces
  `// Set width of progress bars based on data-width attribute`
- Line 133: Indentation over 4 spaces
  `const progressBars = document.querySelectorAll('.progress-bar[data-width]');`
- Line 134: Indentation over 4 spaces
  `progressBars.forEach(bar => {`
- Line 135: Indentation over 4 spaces
  `const width = bar.getAttribute('data-width');`
- Line 136: Indentation over 4 spaces
  `bar.style.width = width + '%';`
- Line 137: Indentation over 4 spaces
  `});`
- Line 138: Indentation over 4 spaces
  `});`
- Line 144: Indentation over 4 spaces
  `.progress {`
- Line 145: Indentation over 4 spaces
  `background-color: #343a40;`
- Line 146: Indentation over 4 spaces
  `}`
- Line 147: Indentation over 4 spaces
  ``
- Line 148: Indentation over 4 spaces
  `.progress-bar {`
- Line 149: Indentation over 4 spaces
  `transition: width 0.3s ease;`
- Line 150: Indentation over 4 spaces
  `}`

### app\templates\cabal\edit.html (47 issues)

#### Best Practice Violations
- Line 7: Indentation over 4 spaces
  `<div class="col-12 mb-4">`
- Line 8: Indentation over 4 spaces
  `<a href="{{ url_for('cabal.index') }}" class="btn btn-outline-secondary mb-3">`
- Line 9: Indentation over 4 spaces
  `<i class="fas fa-arrow-left"></i> Back to Cabal`
- Line 10: Indentation over 4 spaces
  `</a>`
- Line 11: Indentation over 4 spaces
  `<h1 class="pixel-font">Edit Cabal</h1>`
- Line 12: Indentation over 4 spaces
  `<p>Update your cabal's information.</p>`
- Line 13: Indentation over 4 spaces
  `</div>`
- Line 17: Indentation over 4 spaces
  `<div class="col-md-8 offset-md-2">`
- Line 18: Indentation over 4 spaces
  `<div class="card">`
- Line 19: Indentation over 4 spaces
  `<div class="card-header">Edit Cabal Details</div>`
- Line 20: Indentation over 4 spaces
  `<div class="card-body">`
- Line 21: Indentation over 4 spaces
  `<form method="POST" action="{{ url_for('cabal.edit', cabal_id=cabal.id) }}">`
- Line 22: Indentation over 4 spaces
  `<div class="mb-3">`
- Line 23: Indentation over 4 spaces
  `<label for="cabalName" class="form-label">Cabal Name</label>`
- Line 24: Indentation over 4 spaces
  `<input type="text" class="form-control" id="cabalName" name="name" value="{{ cabal.name }}" required>`
- Line 25: Indentation over 4 spaces
  `</div>`
- Line 26: Indentation over 4 spaces
  `<div class="mb-3">`
- Line 27: Indentation over 4 spaces
  `<label for="cabalDescription" class="form-label">Cabal Description</label>`
- Line 28: Indentation over 4 spaces
  `<textarea class="form-control" id="cabalDescription" name="description" rows="4">{{ cabal.description }}</textarea>`
- Line 29: Indentation over 4 spaces
  `</div>`
- Line 30: Indentation over 4 spaces
  ``
- Line 31: Indentation over 4 spaces
  `<div class="mb-3">`
- Line 32: Indentation over 4 spaces
  `<label class="form-label">Invite Code</label>`
- Line 33: Indentation over 4 spaces
  `<div class="input-group">`
- Line 34: Indentation over 4 spaces
  `<input type="text" class="form-control" value="{{ cabal.invite_code }}" readonly>`
- Line 35: Indentation over 4 spaces
  `<button type="button" class="btn btn-outline-primary" onclick="copyToClipboard('{{ cabal.invite_code }}')">`
- Line 36: Indentation over 4 spaces
  `<i class="fas fa-copy"></i> Copy`
- Line 37: Indentation over 4 spaces
  `</button>`
- Line 38: Indentation over 4 spaces
  `</div>`
- Line 39: Indentation over 4 spaces
  `<small class="text-muted">Share this code with others to invite them to your cabal.</small>`
- Line 40: Indentation over 4 spaces
  `</div>`
- Line 41: Indentation over 4 spaces
  ``
- Line 42: Indentation over 4 spaces
  `<div class="d-grid gap-2">`
- Line 43: Indentation over 4 spaces
  `<button type="submit" class="btn btn-pixel">Save Changes</button>`
- Line 44: Indentation over 4 spaces
  `<a href="{{ url_for('cabal.disband', cabal_id=cabal.id) }}" class="btn btn-danger" onclick="return confirm('Are you sure you want to disband the cabal? This action cannot be undone.');">`
- Line 45: Indentation over 4 spaces
  `Disband Cabal`
- Line 46: Indentation over 4 spaces
  `</a>`
- Line 47: Indentation over 4 spaces
  `</div>`
- Line 48: Indentation over 4 spaces
  `</form>`
- Line 49: Indentation over 4 spaces
  `</div>`
- Line 50: Indentation over 4 spaces
  `</div>`
- Line 51: Indentation over 4 spaces
  `</div>`
- Line 58: Indentation over 4 spaces
  `navigator.clipboard.writeText(text).then(function() {`
- Line 59: Indentation over 4 spaces
  `alert('Copied to clipboard!');`
- Line 60: Indentation over 4 spaces
  `}, function(err) {`
- Line 61: Indentation over 4 spaces
  `console.error('Could not copy text: ', err);`
- Line 62: Indentation over 4 spaces
  `});`

### app\templates\cabal\index.html (401 issues)

#### Best Practice Violations
- Line 7: Indentation over 4 spaces
  `{% if cabal %}`
- Line 8: Indentation over 4 spaces
  `<div class="row">`
- Line 9: Indentation over 4 spaces
  `<div class="col-md-8">`
- Line 10: Indentation over 4 spaces
  `<div class="card mb-4">`
- Line 11: Indentation over 4 spaces
  `<div class="card-header bg-dark text-white">`
- Line 12: Indentation over 4 spaces
  `<h3 class="mb-0">{{ cabal.name }} (Level {{ cabal.level }})</h3>`
- Line 13: Indentation over 4 spaces
  `</div>`
- Line 14: Indentation over 4 spaces
  `<div class="card-body">`
- Line 15: Indentation over 4 spaces
  `<p class="lead">{{ cabal.description }}</p>`
- Line 16: Indentation over 4 spaces
  ``
- Line 17: Indentation over 4 spaces
  `<!-- Cabal Stats -->`
- Line 18: Indentation over 4 spaces
  `<div class="row">`
- Line 19: Indentation over 4 spaces
  `<div class="col-md-4">`
- Line 20: Indentation over 4 spaces
  `<h5>Total Power</h5>`
- Line 21: Indentation over 4 spaces
  `<p class="display-6">{{ cabal.total_power|int }}</p>`
- Line 22: Indentation over 4 spaces
  `</div>`
- Line 23: Indentation over 4 spaces
  `<div class="col-md-4">`
- Line 24: Indentation over 4 spaces
  `<h5>Members</h5>`
- Line 25: Indentation over 4 spaces
  `<p class="display-6">{{ cabal.member_count }}/{{ cabal.max_size }}</p>`
- Line 26: Indentation over 4 spaces
  `</div>`
- Line 27: Indentation over 4 spaces
  `<div class="col-md-4">`
- Line 28: Indentation over 4 spaces
  `<h5>Rank</h5>`
- Line 29: Indentation over 4 spaces
  `<p class="display-6">#{{ cabal.rank }}</p>`
- Line 30: Indentation over 4 spaces
  `</div>`
- Line 31: Indentation over 4 spaces
  `</div>`
- Line 32: Indentation over 4 spaces
  ``
- Line 33: Indentation over 4 spaces
  `<hr>`
- Line 34: Indentation over 4 spaces
  ``
- Line 35: Indentation over 4 spaces
  `<!-- Leader Info -->`
- Line 36: Indentation over 4 spaces
  `<div class="d-flex align-items-center mb-3">`
- Line 37: Indentation over 4 spaces
  `<h5 class="me-3 mb-0">Lord of the Shill:</h5>`
- Line 38: Indentation over 4 spaces
  `<span class="badge bg-danger me-2">LORD</span>`
- Line 39: Indentation over 4 spaces
  `<strong>{{ cabal.leader.name }}</strong>`
- Line 40: Indentation over 4 spaces
  `{% if cabal.leader.user %}`
- Line 41: Indentation over 4 spaces
  `(@{{ cabal.leader.user.twitter_handle }})`
- Line 42: Indentation over 4 spaces
  `{% endif %}`
- Line 43: Indentation over 4 spaces
  `</div>`
- Line 44: Indentation over 4 spaces
  ``
- Line 45: Indentation over 4 spaces
  `<!-- Officers -->`
- Line 46: Indentation over 4 spaces
  `<h5>Officers:</h5>`
- Line 47: Indentation over 4 spaces
  `<div class="row mb-3">`
- Line 48: Indentation over 4 spaces
  `{% for role_type, title in [`
- Line 49: Indentation over 4 spaces
  `('clout', 'Duke of Dank Memes'),`
- Line 50: Indentation over 4 spaces
  `('roast_level', 'Earl of Edgelords'),`
- Line 51: Indentation over 4 spaces
  `('cringe_resistance', 'Baron of Bagholders'),`
- Line 52: Indentation over 4 spaces
  `('drip_factor', 'Viscount of Vaporware')`
- Line 53: Indentation over 4 spaces
  `] %}`
- Line 54: Indentation over 4 spaces
  `<div class="col-md-6 mb-2">`
- Line 55: Indentation over 4 spaces
  `<div class="card">`
- Line 56: Indentation over 4 spaces
  `<div class="card-body">`
- Line 57: Indentation over 4 spaces
  `<h6 class="card-title">{{ title }}</h6>`
- Line 58: Indentation over 4 spaces
  `{% if officers and officers.get(role_type) %}`
- Line 59: Indentation over 4 spaces
  `<div class="d-flex align-items-center">`
- Line 60: Indentation over 4 spaces
  `<span class="badge bg-primary me-2">OFFICER</span>`
- Line 61: Indentation over 4 spaces
  `<strong>{{ officers[role_type].name }}</strong>`
- Line 62: Indentation over 4 spaces
  `<small class="ms-1">(@{{ officers[role_type].username }})</small>`
- Line 63: Indentation over 4 spaces
  `{% if is_leader %}`
- Line 64: Indentation over 4 spaces
  `<a href="{{ url_for('cabal.remove_officer', cabal_id=cabal.id, role_type=role_type) }}"`
- Line 65: Indentation over 4 spaces
  `class="btn btn-sm btn-outline-danger ms-auto"`
- Line 66: Indentation over 4 spaces
  `onclick="return confirm('Are you sure you want to remove this officer?')">Remove</a>`
- Line 67: Indentation over 4 spaces
  `{% endif %}`
- Line 68: Indentation over 4 spaces
  `</div>`
- Line 69: Indentation over 4 spaces
  `{% else %}`
- Line 70: Indentation over 4 spaces
  `<p class="card-text text-muted">No officer appointed</p>`
- Line 71: Indentation over 4 spaces
  `{% if is_leader %}`
- Line 72: Indentation over 4 spaces
  `<button type="button" class="btn btn-sm btn-outline-primary"`
- Line 73: Indentation over 4 spaces
  `data-bs-toggle="modal" data-bs-target="#appointOfficerModal"`
- Line 74: Indentation over 4 spaces
  `data-role-type="{{ role_type }}" data-role-title="{{ title }}">`
- Line 75: Indentation over 4 spaces
  `Appoint`
- Line 76: Indentation over 4 spaces
  `</button>`
- Line 77: Indentation over 4 spaces
  `{% endif %}`
- Line 78: Indentation over 4 spaces
  `{% endif %}`
- Line 79: Indentation over 4 spaces
  `</div>`
- Line 80: Indentation over 4 spaces
  `</div>`
- Line 81: Indentation over 4 spaces
  `</div>`
- Line 82: Indentation over 4 spaces
  `{% endfor %}`
- Line 83: Indentation over 4 spaces
  `</div>`
- Line 84: Indentation over 4 spaces
  ``
- Line 85: Indentation over 4 spaces
  `<!-- Invite Code -->`
- Line 86: Indentation over 4 spaces
  `<div class="alert alert-info">`
- Line 87: Indentation over 4 spaces
  `<h5>Invite Code</h5>`
- Line 88: Indentation over 4 spaces
  `<p>Share this code to recruit new members: <strong>{{ cabal.invite_code }}</strong></p>`
- Line 89: Indentation over 4 spaces
  `<p>Or use this link: <code>{{ url_for('cabal.join', code=cabal.invite_code, _external=True) }}</code></p>`
- Line 90: Indentation over 4 spaces
  `</div>`
- Line 91: Indentation over 4 spaces
  ``
- Line 92: Indentation over 4 spaces
  `<!-- Battle Record -->`
- Line 93: Indentation over 4 spaces
  `<div class="mt-3">`
- Line 94: Indentation over 4 spaces
  `<h5>Battle Record</h5>`
- Line 95: Indentation over 4 spaces
  `<div class="row">`
- Line 96: Indentation over 4 spaces
  `<div class="col-md-4">`
- Line 97: Indentation over 4 spaces
  `<p>Wins: <strong>{{ cabal.battles_won }}</strong></p>`
- Line 98: Indentation over 4 spaces
  `</div>`
- Line 99: Indentation over 4 spaces
  `<div class="col-md-4">`
- Line 100: Indentation over 4 spaces
  `<p>Losses: <strong>{{ cabal.battles_lost }}</strong></p>`
- Line 101: Indentation over 4 spaces
  `</div>`
- Line 102: Indentation over 4 spaces
  `<div class="col-md-4">`
- Line 103: Indentation over 4 spaces
  `<p>Win Rate: <strong>`
- Line 104: Indentation over 4 spaces
  `{% if (cabal.battles_won + cabal.battles_lost) > 0 %}`
- Line 105: Indentation over 4 spaces
  `{{ (cabal.battles_won / (cabal.battles_won + cabal.battles_lost) * 100)|round(1) }}%`
- Line 106: Indentation over 4 spaces
  `{% else %}`
- Line 107: Indentation over 4 spaces
  `0%`
- Line 108: Indentation over 4 spaces
  `{% endif %}`
- Line 109: Indentation over 4 spaces
  `</strong></p>`
- Line 110: Indentation over 4 spaces
  `</div>`
- Line 111: Indentation over 4 spaces
  `</div>`
- Line 112: Indentation over 4 spaces
  `</div>`
- Line 113: Indentation over 4 spaces
  ``
- Line 114: Indentation over 4 spaces
  `<!-- Cabal Member Actions -->`
- Line 115: Indentation over 4 spaces
  `<div class="mt-4">`
- Line 116: Indentation over 4 spaces
  `<h5>Member Actions</h5>`
- Line 117: Indentation over 4 spaces
  `<div class="btn-group">`
- Line 118: Indentation over 4 spaces
  `{% if is_leader %}`
- Line 119: Indentation over 4 spaces
  `<a href="{{ url_for('cabal.edit', cabal_id=cabal.id) }}" class="btn btn-outline-primary">Edit Cabal</a>`
- Line 120: Indentation over 4 spaces
  `<a href="{{ url_for('cabal.disband', cabal_id=cabal.id) }}"`
- Line 121: Indentation over 4 spaces
  `class="btn btn-outline-danger"`
- Line 122: Indentation over 4 spaces
  `onclick="return confirm('Are you sure you want to disband this cabal? This action cannot be undone.')">`
- Line 123: Indentation over 4 spaces
  `Disband Cabal`
- Line 124: Indentation over 4 spaces
  `</a>`
- Line 125: Indentation over 4 spaces
  `{% else %}`
- Line 126: Indentation over 4 spaces
  `<a href="{{ url_for('cabal.leave', cabal_id=cabal.id) }}"`
- Line 127: Indentation over 4 spaces
  `class="btn btn-outline-danger"`
- Line 128: Indentation over 4 spaces
  `onclick="return confirm('Are you sure you want to leave this cabal?')">`
- Line 129: Indentation over 4 spaces
  `Leave Cabal`
- Line 130: Indentation over 4 spaces
  `</a>`
- Line 131: Indentation over 4 spaces
  ``
- Line 132: Indentation over 4 spaces
  `{% if not user_voted %}`
- Line 133: Indentation over 4 spaces
  `<a href="{{ url_for('cabal.vote_remove_leader', cabal_id=cabal.id) }}"`
- Line 134: Indentation over 4 spaces
  `class="btn btn-outline-warning"`
- Line 135: Indentation over 4 spaces
  `onclick="return confirm('Are you sure you want to vote to remove the current leader?')">`
- Line 136: Indentation over 4 spaces
  `Vote to Remove Leader`
- Line 137: Indentation over 4 spaces
  `</a>`
- Line 138: Indentation over 4 spaces
  `{% else %}`
- Line 139: Indentation over 4 spaces
  `<button class="btn btn-outline-secondary" disabled>Vote Cast</button>`
- Line 140: Indentation over 4 spaces
  `{% endif %}`
- Line 141: Indentation over 4 spaces
  `{% endif %}`
- Line 142: Indentation over 4 spaces
  `</div>`
- Line 143: Indentation over 4 spaces
  `</div>`
- Line 144: Indentation over 4 spaces
  ``
- Line 145: Indentation over 4 spaces
  `<!-- Leader Vote Status - Only visible to non-leaders -->`
- Line 146: Indentation over 4 spaces
  `{% if not is_leader %}`
- Line 147: Indentation over 4 spaces
  `<div class="mt-3">`
- Line 148: Indentation over 4 spaces
  `<h5>Leader Removal Vote Status</h5>`
- Line 149: Indentation over 4 spaces
  `<div class="progress mb-2">`
- Line 150: Indentation over 4 spaces
  `<div class="progress-bar bg-warning" role="progressbar"`
- Line 151: Indentation over 4 spaces
  `data-width="{{ removal_vote_percentage }}"`
- Line 152: Indentation over 4 spaces
  `aria-valuenow="{{ removal_vote_percentage }}"`
- Line 153: Indentation over 4 spaces
  `aria-valuemin="0" aria-valuemax="100">`
- Line 154: Indentation over 4 spaces
  `{{ removal_vote_percentage|round|int }}%`
- Line 155: Indentation over 4 spaces
  `</div>`
- Line 156: Indentation over 4 spaces
  `</div>`
- Line 157: Indentation over 4 spaces
  `<p class="small text-muted">{{ leader_removal_votes }} out of {{ cabal.get_active_member_count() }} votes`
- Line 158: Indentation over 4 spaces
  `(66% needed to remove leader)</p>`
- Line 159: Indentation over 4 spaces
  `</div>`
- Line 160: Indentation over 4 spaces
  `{% endif %}`
- Line 161: Indentation over 4 spaces
  `</div>`
- Line 162: Indentation over 4 spaces
  `</div>`
- Line 163: Indentation over 4 spaces
  `</div>`
- Line 164: Indentation over 4 spaces
  ``
- Line 165: Indentation over 4 spaces
  `<div class="col-md-4">`
- Line 166: Indentation over 4 spaces
  `<!-- Cabal Benefits Card -->`
- Line 167: Indentation over 4 spaces
  `<div class="card mb-4">`
- Line 168: Indentation over 4 spaces
  `<div class="card-header bg-primary text-white">`
- Line 169: Indentation over 4 spaces
  `<h4 class="mb-0">Cabal Benefits</h4>`
- Line 170: Indentation over 4 spaces
  `</div>`
- Line 171: Indentation over 4 spaces
  `<div class="card-body">`
- Line 172: Indentation over 4 spaces
  `<h5>Active Bonuses</h5>`
- Line 173: Indentation over 4 spaces
  `<ul class="list-group mb-3">`
- Line 174: Indentation over 4 spaces
  `<li class="list-group-item d-flex justify-content-between align-items-center">`
- Line 175: Indentation over 4 spaces
  `Clout Bonus`
- Line 176: Indentation over 4 spaces
  `<span class="badge bg-success">+{{ cabal.clout_bonus }}%</span>`
- Line 177: Indentation over 4 spaces
  `</li>`
- Line 178: Indentation over 4 spaces
  `<li class="list-group-item d-flex justify-content-between align-items-center">`
- Line 179: Indentation over 4 spaces
  `Roast Damage`
- Line 180: Indentation over 4 spaces
  `<span class="badge bg-danger">+{{ cabal.roast_bonus }}%</span>`
- Line 181: Indentation over 4 spaces
  `</li>`
- Line 182: Indentation over 4 spaces
  `<li class="list-group-item d-flex justify-content-between align-items-center">`
- Line 183: Indentation over 4 spaces
  `Cringe Defense`
- Line 184: Indentation over 4 spaces
  `<span class="badge bg-info">+{{ cabal.cringe_bonus }}%</span>`
- Line 185: Indentation over 4 spaces
  `</li>`
- Line 186: Indentation over 4 spaces
  `<li class="list-group-item d-flex justify-content-between align-items-center">`
- Line 187: Indentation over 4 spaces
  `Drip Bonus`
- Line 188: Indentation over 4 spaces
  `<span class="badge bg-warning text-dark">+{{ cabal.drip_bonus }}%</span>`
- Line 189: Indentation over 4 spaces
  `</li>`
- Line 190: Indentation over 4 spaces
  `</ul>`
- Line 191: Indentation over 4 spaces
  ``
- Line 192: Indentation over 4 spaces
  `<p class="text-muted">Bonuses are calculated based on officer stats and cabal level.</p>`
- Line 193: Indentation over 4 spaces
  `</div>`
- Line 194: Indentation over 4 spaces
  `</div>`
- Line 195: Indentation over 4 spaces
  ``
- Line 196: Indentation over 4 spaces
  `<!-- Upcoming Battles Card -->`
- Line 197: Indentation over 4 spaces
  `<div class="card mb-4">`
- Line 198: Indentation over 4 spaces
  `<div class="card-header bg-danger text-white">`
- Line 199: Indentation over 4 spaces
  `<h4 class="mb-0">Upcoming Battles</h4>`
- Line 200: Indentation over 4 spaces
  `</div>`
- Line 201: Indentation over 4 spaces
  `<div class="card-body">`
- Line 202: Indentation over 4 spaces
  `{% if is_leader %}`
- Line 203: Indentation over 4 spaces
  `<a href="{{ url_for('cabal.schedule_battle', cabal_id=cabal.id) }}" class="btn btn-outline-danger mb-3">Schedule New Battle</a>`
- Line 204: Indentation over 4 spaces
  `{% endif %}`
- Line 205: Indentation over 4 spaces
  ``
- Line 206: Indentation over 4 spaces
  `<a href="{{ url_for('cabal.all_battles') }}" class="btn btn-outline-secondary mb-3">View All Battles</a>`
- Line 207: Indentation over 4 spaces
  ``
- Line 208: Indentation over 4 spaces
  `{% if upcoming_battles %}`
- Line 209: Indentation over 4 spaces
  `<div class="list-group">`
- Line 210: Indentation over 4 spaces
  `{% for battle in upcoming_battles %}`
- Line 211: Indentation over 4 spaces
  `<div class="list-group-item">`
- Line 212: Indentation over 4 spaces
  `<div class="d-flex w-100 justify-content-between">`
- Line 213: Indentation over 4 spaces
  `<h5 class="mb-1">vs. {{ battle.opponent_cabal.name }}</h5>`
- Line 214: Indentation over 4 spaces
  `<small>`
- Line 215: Indentation over 4 spaces
  `{% set time_diff = (battle.scheduled_at - now).total_seconds() %}`
- Line 216: Indentation over 4 spaces
  `{% if time_diff < 3600 %}`
- Line 217: Indentation over 4 spaces
  `<span class="text-danger">{{ (time_diff / 60)|int }} minutes</span>`
- Line 218: Indentation over 4 spaces
  `{% elif time_diff < 86400 %}`
- Line 219: Indentation over 4 spaces
  `<span class="text-warning">{{ (time_diff / 3600)|int }} hours</span>`
- Line 220: Indentation over 4 spaces
  `{% else %}`
- Line 221: Indentation over 4 spaces
  `<span class="text-info">{{ (time_diff / 86400)|int }} days</span>`
- Line 222: Indentation over 4 spaces
  `{% endif %}`
- Line 223: Indentation over 4 spaces
  `</small>`
- Line 224: Indentation over 4 spaces
  `</div>`
- Line 225: Indentation over 4 spaces
  `<p class="mb-1">{{ battle.scheduled_at.strftime('%Y-%m-%d %H:%M UTC') }}</p>`
- Line 226: Indentation over 4 spaces
  `<small>{{ battle.participant_count }} members participating</small>`
- Line 227: Indentation over 4 spaces
  ``
- Line 228: Indentation over 4 spaces
  `{% set user_participating = battle.is_user_participating(current_user.chad.id) %}`
- Line 229: Indentation over 4 spaces
  ``
- Line 230: Indentation over 4 spaces
  `{% if not user_participating %}`
- Line 231: Indentation over 4 spaces
  `<a href="{{ url_for('cabal.opt_into_battle', battle_id=battle.id) }}"`
- Line 232: Indentation over 4 spaces
  `class="btn btn-sm btn-success mt-2">Opt In</a>`
- Line 233: Indentation over 4 spaces
  `{% else %}`
- Line 234: Indentation over 4 spaces
  `<span class="badge bg-success mt-2">You're In</span>`
- Line 235: Indentation over 4 spaces
  `{% endif %}`
- Line 236: Indentation over 4 spaces
  `</div>`
- Line 237: Indentation over 4 spaces
  `{% endfor %}`
- Line 238: Indentation over 4 spaces
  `</div>`
- Line 239: Indentation over 4 spaces
  `{% else %}`
- Line 240: Indentation over 4 spaces
  `<p class="text-muted">No upcoming battles scheduled.</p>`
- Line 241: Indentation over 4 spaces
  `{% endif %}`
- Line 242: Indentation over 4 spaces
  `</div>`
- Line 243: Indentation over 4 spaces
  `</div>`
- Line 244: Indentation over 4 spaces
  `</div>`
- Line 245: Indentation over 4 spaces
  `</div>`
- Line 246: Indentation over 4 spaces
  ``
- Line 247: Indentation over 4 spaces
  `<!-- Appoint Officer Modal -->`
- Line 248: Indentation over 4 spaces
  `<div class="modal fade" id="appointOfficerModal" tabindex="-1" aria-labelledby="appointOfficerModalLabel" aria-hidden="true">`
- Line 249: Indentation over 4 spaces
  `<div class="modal-dialog">`
- Line 250: Indentation over 4 spaces
  `<div class="modal-content">`
- Line 251: Indentation over 4 spaces
  `<div class="modal-header">`
- Line 252: Indentation over 4 spaces
  `<h5 class="modal-title" id="appointOfficerModalLabel">Appoint Officer</h5>`
- Line 253: Indentation over 4 spaces
  `<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>`
- Line 254: Indentation over 4 spaces
  `</div>`
- Line 255: Indentation over 4 spaces
  `<div class="modal-body">`
- Line 256: Indentation over 4 spaces
  `<form action="{{ url_for('cabal.appoint_officer', cabal_id=cabal.id) }}" method="POST">`
- Line 257: Indentation over 4 spaces
  `<input type="hidden" name="role_type" id="role_type">`
- Line 258: Indentation over 4 spaces
  `<div class="mb-3">`
- Line 259: Indentation over 4 spaces
  `<h5 id="role_title"></h5>`
- Line 260: Indentation over 4 spaces
  `<p class="text-muted" id="role_description"></p>`
- Line 261: Indentation over 4 spaces
  `</div>`
- Line 262: Indentation over 4 spaces
  `<div class="mb-3">`
- Line 263: Indentation over 4 spaces
  `<label for="chad_id" class="form-label">Select Member</label>`
- Line 264: Indentation over 4 spaces
  `<select class="form-select" id="chad_id" name="chad_id" required>`
- Line 265: Indentation over 4 spaces
  `<option value="">Select a member...</option>`
- Line 266: Indentation over 4 spaces
  `{% for member in cabal.members %}`
- Line 267: Indentation over 4 spaces
  `{% if member.chad_id != cabal.leader_id %}`
- Line 268: Indentation over 4 spaces
  `<option value="{{ member.chad_id }}">{{ member.chad.name }}</option>`
- Line 269: Indentation over 4 spaces
  `{% endif %}`
- Line 270: Indentation over 4 spaces
  `{% endfor %}`
- Line 271: Indentation over 4 spaces
  `</select>`
- Line 272: Indentation over 4 spaces
  `</div>`
- Line 273: Indentation over 4 spaces
  `<div class="d-grid">`
- Line 274: Indentation over 4 spaces
  `<button type="submit" class="btn btn-primary">Appoint Officer</button>`
- Line 275: Indentation over 4 spaces
  `</div>`
- Line 276: Indentation over 4 spaces
  `</form>`
- Line 277: Indentation over 4 spaces
  `</div>`
- Line 278: Indentation over 4 spaces
  `</div>`
- Line 279: Indentation over 4 spaces
  `</div>`
- Line 280: Indentation over 4 spaces
  `</div>`
- Line 281: Indentation over 4 spaces
  ``
- Line 282: Indentation over 4 spaces
  `<script>`
- Line 283: Indentation over 4 spaces
  `document.addEventListener('DOMContentLoaded', function() {`
- Line 284: Indentation over 4 spaces
  `// Officer role selection`
- Line 285: Indentation over 4 spaces
  `const roleSelect = document.getElementById('officer_role');`
- Line 286: Indentation over 4 spaces
  `if (roleSelect) {`
- Line 287: Indentation over 4 spaces
  `roleSelect.addEventListener('change', function() {`
- Line 288: Indentation over 4 spaces
  `const role = this.value;`
- Line 289: Indentation over 4 spaces
  `let description = '';`
- Line 290: Indentation over 4 spaces
  `switch(role) {`
- Line 291: Indentation over 4 spaces
  `case 'clout':`
- Line 292: Indentation over 4 spaces
  `description = 'Increases cabal XP gain from activities';`
- Line 293: Indentation over 4 spaces
  `break;`
- Line 294: Indentation over 4 spaces
  `case 'roast_level':`
- Line 295: Indentation over 4 spaces
  `description = 'Boosts attack damage in battles';`
- Line 296: Indentation over 4 spaces
  `break;`
- Line 297: Indentation over 4 spaces
  `case 'cringe_resistance':`
- Line 298: Indentation over 4 spaces
  `description = 'Improves defense against attacks';`
- Line 299: Indentation over 4 spaces
  `break;`
- Line 300: Indentation over 4 spaces
  `case 'drip_factor':`
- Line 301: Indentation over 4 spaces
  `description = 'Enhances reward drops after victories';`
- Line 302: Indentation over 4 spaces
  `break;`
- Line 303: Indentation over 4 spaces
  `}`
- Line 304: Indentation over 4 spaces
  `document.getElementById('role_description').textContent = description;`
- Line 305: Indentation over 4 spaces
  `});`
- Line 306: Indentation over 4 spaces
  `}`
- Line 308: Indentation over 4 spaces
  `// Set width of progress bars based on data-width attribute`
- Line 309: Indentation over 4 spaces
  `const progressBars = document.querySelectorAll('.progress-bar[data-width]');`
- Line 310: Indentation over 4 spaces
  `progressBars.forEach(bar => {`
- Line 311: Indentation over 4 spaces
  `const width = bar.getAttribute('data-width');`
- Line 312: Indentation over 4 spaces
  `bar.style.width = width + '%';`
- Line 313: Indentation over 4 spaces
  `});`
- Line 314: Indentation over 4 spaces
  `});`
- Line 315: Indentation over 4 spaces
  `</script>`
- Line 316: Indentation over 4 spaces
  `{% else %}`
- Line 317: Indentation over 4 spaces
  `<div class="card">`
- Line 318: Indentation over 4 spaces
  `<div class="card-header bg-dark text-white">`
- Line 319: Indentation over 4 spaces
  `<h3 class="mb-0">Join a Cabal</h3>`
- Line 320: Indentation over 4 spaces
  `</div>`
- Line 321: Indentation over 4 spaces
  `<div class="card-body">`
- Line 322: Indentation over 4 spaces
  `<p class="lead">You are not currently in a cabal. Join an existing cabal or create your own!</p>`
- Line 323: Indentation over 4 spaces
  ``
- Line 324: Indentation over 4 spaces
  `<div class="row mt-4">`
- Line 325: Indentation over 4 spaces
  `<div class="col-md-6">`
- Line 326: Indentation over 4 spaces
  `<div class="card mb-3">`
- Line 327: Indentation over 4 spaces
  `<div class="card-header bg-primary text-white">`
- Line 328: Indentation over 4 spaces
  `<h4>Create Your Own Cabal</h4>`
- Line 329: Indentation over 4 spaces
  `</div>`
- Line 330: Indentation over 4 spaces
  `<div class="card-body">`
- Line 331: Indentation over 4 spaces
  `<p>Form your own cabal and become the Lord of the Shill. Recruit members and battle other cabals for glory!</p>`
- Line 332: Indentation over 4 spaces
  `<a href="{{ url_for('cabal.create') }}" class="btn btn-primary">Create Cabal</a>`
- Line 333: Indentation over 4 spaces
  `</div>`
- Line 334: Indentation over 4 spaces
  `</div>`
- Line 335: Indentation over 4 spaces
  `</div>`
- Line 336: Indentation over 4 spaces
  ``
- Line 337: Indentation over 4 spaces
  `<div class="col-md-6">`
- Line 338: Indentation over 4 spaces
  `<div class="card">`
- Line 339: Indentation over 4 spaces
  `<div class="card-header bg-success text-white">`
- Line 340: Indentation over 4 spaces
  `<h4>Join Existing Cabal</h4>`
- Line 341: Indentation over 4 spaces
  `</div>`
- Line 342: Indentation over 4 spaces
  `<div class="card-body">`
- Line 343: Indentation over 4 spaces
  `<p>Join an existing cabal with an invite code.</p>`
- Line 344: Indentation over 4 spaces
  `<form action="{{ url_for('cabal.join') }}" method="POST">`
- Line 345: Indentation over 4 spaces
  `<div class="input-group mb-3">`
- Line 346: Indentation over 4 spaces
  `<input type="text" class="form-control" placeholder="Enter invite code" name="invite_code" required>`
- Line 347: Indentation over 4 spaces
  `<button class="btn btn-success" type="submit">Join</button>`
- Line 348: Indentation over 4 spaces
  `</div>`
- Line 349: Indentation over 4 spaces
  `</form>`
- Line 350: Indentation over 4 spaces
  `</div>`
- Line 351: Indentation over 4 spaces
  `</div>`
- Line 352: Indentation over 4 spaces
  `</div>`
- Line 353: Indentation over 4 spaces
  `</div>`
- Line 354: Indentation over 4 spaces
  ``
- Line 355: Indentation over 4 spaces
  `<div class="mt-4">`
- Line 356: Indentation over 4 spaces
  `<a href="{{ url_for('cabal.leaderboard') }}" class="btn btn-outline-dark">View Cabal Leaderboard</a>`
- Line 357: Indentation over 4 spaces
  `</div>`
- Line 358: Indentation over 4 spaces
  `</div>`
- Line 359: Indentation over 4 spaces
  `</div>`
- Line 360: Indentation over 4 spaces
  `{% endif %}`
- Line 366: Indentation over 4 spaces
  `function preSelectRole(roleType) {`
- Line 367: Indentation over 4 spaces
  `document.getElementById('roleSelect').value = roleType;`
- Line 368: Indentation over 4 spaces
  `}`
- Line 369: Indentation over 4 spaces
  ``
- Line 370: Indentation over 4 spaces
  `function preSelectMember(chadId) {`
- Line 371: Indentation over 4 spaces
  `document.getElementById('memberSelect').value = chadId;`
- Line 372: Indentation over 4 spaces
  `}`
- Line 378: Indentation over 4 spaces
  `.cabal-level-badge {`
- Line 379: Indentation over 4 spaces
  `width: 50px;`
- Line 380: Indentation over 4 spaces
  `height: 50px;`
- Line 381: Indentation over 4 spaces
  `background-color: #ffc107;`
- Line 382: Indentation over 4 spaces
  `color: #000;`
- Line 383: Indentation over 4 spaces
  `font-weight: bold;`
- Line 384: Indentation over 4 spaces
  `font-size: 24px;`
- Line 385: Indentation over 4 spaces
  `display: flex;`
- Line 386: Indentation over 4 spaces
  `align-items: center;`
- Line 387: Indentation over 4 spaces
  `justify-content: center;`
- Line 388: Indentation over 4 spaces
  `border-radius: 50%;`
- Line 389: Indentation over 4 spaces
  `}`
- Line 390: Indentation over 4 spaces
  ``
- Line 391: Indentation over 4 spaces
  `.leadership-avatar {`
- Line 392: Indentation over 4 spaces
  `width: 60px;`
- Line 393: Indentation over 4 spaces
  `height: 60px;`
- Line 394: Indentation over 4 spaces
  `border-radius: 50%;`
- Line 395: Indentation over 4 spaces
  `display: flex;`
- Line 396: Indentation over 4 spaces
  `align-items: center;`
- Line 397: Indentation over 4 spaces
  `justify-content: center;`
- Line 398: Indentation over 4 spaces
  `font-size: 24px;`
- Line 399: Indentation over 4 spaces
  `margin: 0 auto;`
- Line 400: Indentation over 4 spaces
  `}`
- Line 401: Indentation over 4 spaces
  ``
- Line 402: Indentation over 4 spaces
  `.leadership-avatar.lord {`
- Line 403: Indentation over 4 spaces
  `background-color: #ffc107;`
- Line 404: Indentation over 4 spaces
  `color: #000;`
- Line 405: Indentation over 4 spaces
  `}`
- Line 406: Indentation over 4 spaces
  ``
- Line 407: Indentation over 4 spaces
  `.leadership-avatar.officer {`
- Line 408: Indentation over 4 spaces
  `background-color: #17a2b8;`
- Line 409: Indentation over 4 spaces
  `color: #fff;`
- Line 410: Indentation over 4 spaces
  `}`
- Line 411: Indentation over 4 spaces
  ``
- Line 412: Indentation over 4 spaces
  `.role-bonus {`
- Line 413: Indentation over 4 spaces
  `margin-top: 8px;`
- Line 414: Indentation over 4 spaces
  `}`
- Line 415: Indentation over 4 spaces
  ``
- Line 416: Indentation over 4 spaces
  `.leader-name, .officer-name {`
- Line 417: Indentation over 4 spaces
  `font-weight: bold;`
- Line 418: Indentation over 4 spaces
  `}`

### app\templates\cabal\leaderboard.html (135 issues)

#### Best Practice Violations
- Line 7: Indentation over 4 spaces
  `<div class="col-12 mb-4">`
- Line 8: Indentation over 4 spaces
  `<h1 class="pixel-font">Cabal Leaderboard</h1>`
- Line 9: Indentation over 4 spaces
  `<p class="lead">The most powerful cabals in the Chad Battles universe!</p>`
- Line 10: Indentation over 4 spaces
  `</div>`
- Line 14: Indentation over 4 spaces
  `<div class="col-md-12">`
- Line 15: Indentation over 4 spaces
  `<div class="card">`
- Line 16: Indentation over 4 spaces
  `<div class="card-header d-flex justify-content-between align-items-center">`
- Line 17: Indentation over 4 spaces
  `<span>Top Cabals</span>`
- Line 18: Indentation over 4 spaces
  `{% if current_user.is_authenticated and current_user.chad %}`
- Line 19: Indentation over 4 spaces
  `{% if current_user.chad.cabal_membership %}`
- Line 20: Indentation over 4 spaces
  `<a href="{{ url_for('cabal.index') }}" class="btn btn-sm btn-pixel">My Cabal</a>`
- Line 21: Indentation over 4 spaces
  `{% else %}`
- Line 22: Indentation over 4 spaces
  `<a href="{{ url_for('cabal.create') }}" class="btn btn-sm btn-pixel">Create Cabal</a>`
- Line 23: Indentation over 4 spaces
  `{% endif %}`
- Line 24: Indentation over 4 spaces
  `{% endif %}`
- Line 25: Indentation over 4 spaces
  `</div>`
- Line 26: Indentation over 4 spaces
  `<div class="card-body">`
- Line 27: Indentation over 4 spaces
  `{% if cabals %}`
- Line 28: Indentation over 4 spaces
  `<div class="table-responsive">`
- Line 29: Indentation over 4 spaces
  `<table class="table table-dark table-hover">`
- Line 30: Indentation over 4 spaces
  `<thead>`
- Line 31: Indentation over 4 spaces
  `<tr>`
- Line 32: Indentation over 4 spaces
  `<th>Rank</th>`
- Line 33: Indentation over 4 spaces
  `<th>Cabal</th>`
- Line 34: Indentation over 4 spaces
  `<th>Level</th>`
- Line 35: Indentation over 4 spaces
  `<th>Battle Power</th>`
- Line 36: Indentation over 4 spaces
  `<th>Members</th>`
- Line 37: Indentation over 4 spaces
  `<th>Lord of the Shill</th>`
- Line 38: Indentation over 4 spaces
  `<th>W/L</th>`
- Line 39: Indentation over 4 spaces
  `<th>Win Rate</th>`
- Line 40: Indentation over 4 spaces
  `</tr>`
- Line 41: Indentation over 4 spaces
  `</thead>`
- Line 42: Indentation over 4 spaces
  `<tbody>`
- Line 43: Indentation over 4 spaces
  `{% for cabal in cabals %}`
- Line 44: Indentation over 4 spaces
  `<tr>`
- Line 45: Indentation over 4 spaces
  `<td>{{ cabal.rank }}</td>`
- Line 46: Indentation over 4 spaces
  `<td>`
- Line 47: Indentation over 4 spaces
  `<a href="{{ url_for('cabal.battles', cabal_id=cabal.id) }}" class="cabal-name">{{ cabal.name }}</a>`
- Line 48: Indentation over 4 spaces
  `</td>`
- Line 49: Indentation over 4 spaces
  `<td>{{ cabal.level }}</td>`
- Line 50: Indentation over 4 spaces
  `<td>{{ cabal.power | number_format }}</td>`
- Line 51: Indentation over 4 spaces
  `<td>{{ cabal.member_count }}</td>`
- Line 52: Indentation over 4 spaces
  `<td>`
- Line 53: Indentation over 4 spaces
  `<span class="leader-name">{{ cabal.leader_name }}</span>`
- Line 54: Indentation over 4 spaces
  `<small class="text-muted d-block">@{{ cabal.leader_username }}</small>`
- Line 55: Indentation over 4 spaces
  `</td>`
- Line 56: Indentation over 4 spaces
  `<td>{{ cabal.battles_won }}/{{ cabal.battles_lost }}</td>`
- Line 57: Indentation over 4 spaces
  `<td>`
- Line 58: Indentation over 4 spaces
  `<div class="progress" style="height: 20px;">`
- Line 59: Indentation over 4 spaces
  `<div class="progress-bar bg-success" role="progressbar"`
- Line 60: Indentation over 4 spaces
  `data-width="{{ cabal.win_rate }}"`
- Line 61: Indentation over 4 spaces
  `aria-valuenow="{{ cabal.win_rate }}"`
- Line 62: Indentation over 4 spaces
  `aria-valuemin="0"`
- Line 63: Indentation over 4 spaces
  `aria-valuemax="100">`
- Line 64: Indentation over 4 spaces
  `{{ cabal.win_rate }}%`
- Line 65: Indentation over 4 spaces
  `</div>`
- Line 66: Indentation over 4 spaces
  `</div>`
- Line 67: Indentation over 4 spaces
  `</td>`
- Line 68: Indentation over 4 spaces
  `</tr>`
- Line 69: Indentation over 4 spaces
  `{% endfor %}`
- Line 70: Indentation over 4 spaces
  `</tbody>`
- Line 71: Indentation over 4 spaces
  `</table>`
- Line 72: Indentation over 4 spaces
  `</div>`
- Line 73: Indentation over 4 spaces
  `{% else %}`
- Line 74: Indentation over 4 spaces
  `<div class="alert alert-info">`
- Line 75: Indentation over 4 spaces
  `<p>No cabals found. Be the first to create one!</p>`
- Line 76: Indentation over 4 spaces
  `{% if current_user.is_authenticated and current_user.chad %}`
- Line 77: Indentation over 4 spaces
  `<a href="{{ url_for('cabal.create') }}" class="btn btn-pixel mt-2">Create Cabal</a>`
- Line 78: Indentation over 4 spaces
  `{% endif %}`
- Line 79: Indentation over 4 spaces
  `</div>`
- Line 80: Indentation over 4 spaces
  `{% endif %}`
- Line 81: Indentation over 4 spaces
  `</div>`
- Line 82: Indentation over 4 spaces
  `</div>`
- Line 83: Indentation over 4 spaces
  `</div>`
- Line 87: Indentation over 4 spaces
  `<div class="col-md-6">`
- Line 88: Indentation over 4 spaces
  `<div class="card mb-4">`
- Line 89: Indentation over 4 spaces
  `<div class="card-header">Cabal Perks</div>`
- Line 90: Indentation over 4 spaces
  `<div class="card-body">`
- Line 91: Indentation over 4 spaces
  `<h5 class="pixel-font">Why Join a Cabal?</h5>`
- Line 92: Indentation over 4 spaces
  `<ul>`
- Line 93: Indentation over 4 spaces
  `<li>Gain stat bonuses from the Lord of the Shill and Officers</li>`
- Line 94: Indentation over 4 spaces
  `<li>Participate in cabal battles for bonus XP and rewards</li>`
- Line 95: Indentation over 4 spaces
  `<li>Climb the leaderboard ranks together</li>`
- Line 96: Indentation over 4 spaces
  `<li>Access to special cabal-only missions and events</li>`
- Line 97: Indentation over 4 spaces
  `<li>Form alliances with other cabals for strategic advantage</li>`
- Line 98: Indentation over 4 spaces
  `</ul>`
- Line 99: Indentation over 4 spaces
  `</div>`
- Line 100: Indentation over 4 spaces
  `</div>`
- Line 101: Indentation over 4 spaces
  `</div>`
- Line 102: Indentation over 4 spaces
  ``
- Line 103: Indentation over 4 spaces
  `<div class="col-md-6">`
- Line 104: Indentation over 4 spaces
  `<div class="card mb-4">`
- Line 105: Indentation over 4 spaces
  `<div class="card-header">Officer System</div>`
- Line 106: Indentation over 4 spaces
  `<div class="card-body">`
- Line 107: Indentation over 4 spaces
  `<h5 class="pixel-font">Cabal Officers</h5>`
- Line 108: Indentation over 4 spaces
  `<p>Each cabal can have four officers, each granting bonuses to all members:</p>`
- Line 109: Indentation over 4 spaces
  `<ul>`
- Line 110: Indentation over 4 spaces
  `<li><strong>Clout Commander:</strong> Grants 50% of their Clout stat to all cabal members</li>`
- Line 111: Indentation over 4 spaces
  `<li><strong>Roast Master:</strong> Grants 50% of their Roast Level stat to all cabal members</li>`
- Line 112: Indentation over 4 spaces
  `<li><strong>Cringe Shield:</strong> Grants 50% of their Cringe Resistance stat to all cabal members</li>`
- Line 113: Indentation over 4 spaces
  `<li><strong>Drip Director:</strong> Grants 50% of their Drip Factor stat to all cabal members</li>`
- Line 114: Indentation over 4 spaces
  `</ul>`
- Line 115: Indentation over 4 spaces
  `<p class="text-muted">The Lord of the Shill also grants 0.1 to all stats for every cabal member.</p>`
- Line 116: Indentation over 4 spaces
  `</div>`
- Line 117: Indentation over 4 spaces
  `</div>`
- Line 118: Indentation over 4 spaces
  `</div>`
- Line 124: Indentation over 4 spaces
  `document.addEventListener('DOMContentLoaded', function() {`
- Line 125: Indentation over 4 spaces
  `// Set width of progress bars based on data-width attribute`
- Line 126: Indentation over 4 spaces
  `const progressBars = document.querySelectorAll('.progress-bar[data-width]');`
- Line 127: Indentation over 4 spaces
  `progressBars.forEach(bar => {`
- Line 128: Indentation over 4 spaces
  `const width = bar.getAttribute('data-width');`
- Line 129: Indentation over 4 spaces
  `bar.style.width = width + '%';`
- Line 130: Indentation over 4 spaces
  `});`
- Line 131: Indentation over 4 spaces
  `});`
- Line 137: Indentation over 4 spaces
  `.cabal-name {`
- Line 138: Indentation over 4 spaces
  `color: #ffc107;`
- Line 139: Indentation over 4 spaces
  `font-weight: bold;`
- Line 140: Indentation over 4 spaces
  `}`
- Line 141: Indentation over 4 spaces
  ``
- Line 142: Indentation over 4 spaces
  `.cabal-name:hover {`
- Line 143: Indentation over 4 spaces
  `color: #ffc107;`
- Line 144: Indentation over 4 spaces
  `text-decoration: none;`
- Line 145: Indentation over 4 spaces
  `}`
- Line 146: Indentation over 4 spaces
  ``
- Line 147: Indentation over 4 spaces
  `.leader-name {`
- Line 148: Indentation over 4 spaces
  `font-weight: bold;`
- Line 149: Indentation over 4 spaces
  `}`
- Line 150: Indentation over 4 spaces
  ``
- Line 151: Indentation over 4 spaces
  `.progress {`
- Line 152: Indentation over 4 spaces
  `background-color: #343a40;`
- Line 153: Indentation over 4 spaces
  `}`
- Line 154: Indentation over 4 spaces
  ``
- Line 155: Indentation over 4 spaces
  `.progress-bar {`
- Line 156: Indentation over 4 spaces
  `transition: width 0.3s ease;`
- Line 157: Indentation over 4 spaces
  `}`

### app\templates\cabal\schedule_battle.html (98 issues)

#### Best Practice Violations
- Line 7: Indentation over 4 spaces
  `<div class="col-12 mb-4">`
- Line 8: Indentation over 4 spaces
  `<a href="{{ url_for('cabal.index') }}" class="btn btn-outline-secondary mb-3">`
- Line 9: Indentation over 4 spaces
  `<i class="fas fa-arrow-left"></i> Back to Cabal`
- Line 10: Indentation over 4 spaces
  `</a>`
- Line 11: Indentation over 4 spaces
  `<h1 class="pixel-font">Schedule Cabal Battle</h1>`
- Line 12: Indentation over 4 spaces
  `<p>Challenge another cabal to battle and increase your cabal's glory!</p>`
- Line 13: Indentation over 4 spaces
  `</div>`
- Line 17: Indentation over 4 spaces
  `<div class="col-md-8">`
- Line 18: Indentation over 4 spaces
  `<div class="card mb-4">`
- Line 19: Indentation over 4 spaces
  `<div class="card-header">Battle Schedule</div>`
- Line 20: Indentation over 4 spaces
  `<div class="card-body">`
- Line 21: Indentation over 4 spaces
  `{% if battles_remaining > 0 %}`
- Line 22: Indentation over 4 spaces
  `<p>Your cabal can schedule <strong>{{ battles_remaining }}</strong> more battles this week.</p>`
- Line 23: Indentation over 4 spaces
  ``
- Line 24: Indentation over 4 spaces
  `<form method="POST" action="{{ url_for('cabal.schedule_battle', cabal_id=cabal.id) }}">`
- Line 25: Indentation over 4 spaces
  `<div class="mb-3">`
- Line 26: Indentation over 4 spaces
  `<label for="opponentCabal" class="form-label">Select Opponent Cabal</label>`
- Line 27: Indentation over 4 spaces
  `<select class="form-select" id="opponentCabal" name="opponent_cabal_id" required>`
- Line 28: Indentation over 4 spaces
  `<option value="" selected disabled>-- Select Opponent --</option>`
- Line 29: Indentation over 4 spaces
  `{% for opponent in other_cabals %}`
- Line 30: Indentation over 4 spaces
  `<option value="{{ opponent.id }}">{{ opponent.name }} (Level {{ opponent.level }})</option>`
- Line 31: Indentation over 4 spaces
  `{% endfor %}`
- Line 32: Indentation over 4 spaces
  `</select>`
- Line 33: Indentation over 4 spaces
  `</div>`
- Line 34: Indentation over 4 spaces
  ``
- Line 35: Indentation over 4 spaces
  `<div class="row mb-3">`
- Line 36: Indentation over 4 spaces
  `<div class="col-md-6">`
- Line 37: Indentation over 4 spaces
  `<label for="battleDate" class="form-label">Battle Date</label>`
- Line 38: Indentation over 4 spaces
  `<input type="date" class="form-control" id="battleDate" name="battle_date" required min="{{ now.strftime('%Y-%m-%d') }}">`
- Line 39: Indentation over 4 spaces
  `</div>`
- Line 40: Indentation over 4 spaces
  `<div class="col-md-6">`
- Line 41: Indentation over 4 spaces
  `<label for="battleTime" class="form-label">Battle Time (UTC)</label>`
- Line 42: Indentation over 4 spaces
  `<input type="time" class="form-control" id="battleTime" name="battle_time" required>`
- Line 43: Indentation over 4 spaces
  `</div>`
- Line 44: Indentation over 4 spaces
  `</div>`
- Line 45: Indentation over 4 spaces
  ``
- Line 46: Indentation over 4 spaces
  `<div class="alert alert-info">`
- Line 47: Indentation over 4 spaces
  `<i class="fas fa-info-circle"></i> Battles must be scheduled at least 1 hour in the future to allow members time to opt in.`
- Line 48: Indentation over 4 spaces
  `</div>`
- Line 49: Indentation over 4 spaces
  ``
- Line 50: Indentation over 4 spaces
  `<div class="d-grid">`
- Line 51: Indentation over 4 spaces
  `<button type="submit" class="btn btn-pixel">Schedule Battle</button>`
- Line 52: Indentation over 4 spaces
  `</div>`
- Line 53: Indentation over 4 spaces
  `</form>`
- Line 54: Indentation over 4 spaces
  `{% else %}`
- Line 55: Indentation over 4 spaces
  `<div class="alert alert-warning">`
- Line 56: Indentation over 4 spaces
  `<i class="fas fa-exclamation-triangle"></i> Your cabal has already scheduled the maximum 3 battles for this week.`
- Line 57: Indentation over 4 spaces
  `</div>`
- Line 58: Indentation over 4 spaces
  `<p>Try again next week, or focus on the battles you've already scheduled!</p>`
- Line 59: Indentation over 4 spaces
  `{% endif %}`
- Line 60: Indentation over 4 spaces
  `</div>`
- Line 61: Indentation over 4 spaces
  `</div>`
- Line 62: Indentation over 4 spaces
  `</div>`
- Line 63: Indentation over 4 spaces
  ``
- Line 64: Indentation over 4 spaces
  `<div class="col-md-4">`
- Line 65: Indentation over 4 spaces
  `<div class="card mb-4">`
- Line 66: Indentation over 4 spaces
  `<div class="card-header">Battle Tips</div>`
- Line 67: Indentation over 4 spaces
  `<div class="card-body">`
- Line 68: Indentation over 4 spaces
  `<h5 class="pixel-font">For Maximum Success:</h5>`
- Line 69: Indentation over 4 spaces
  `<ul>`
- Line 70: Indentation over 4 spaces
  `<li>Encourage all cabal members to opt in</li>`
- Line 71: Indentation over 4 spaces
  `<li>Challenge cabals near your own level</li>`
- Line 72: Indentation over 4 spaces
  `<li>Make sure your officers are optimized for their roles</li>`
- Line 73: Indentation over 4 spaces
  `<li>Schedule battles when most of your members are available</li>`
- Line 74: Indentation over 4 spaces
  `<li>Use Meme Elixirs before important battles</li>`
- Line 75: Indentation over 4 spaces
  `</ul>`
- Line 76: Indentation over 4 spaces
  `</div>`
- Line 77: Indentation over 4 spaces
  `</div>`
- Line 78: Indentation over 4 spaces
  ``
- Line 79: Indentation over 4 spaces
  `<div class="card">`
- Line 80: Indentation over 4 spaces
  `<div class="card-header">Rewards</div>`
- Line 81: Indentation over 4 spaces
  `<div class="card-body">`
- Line 82: Indentation over 4 spaces
  `<h5 class="pixel-font">Battle Victory Yields:</h5>`
- Line 83: Indentation over 4 spaces
  `<ul>`
- Line 84: Indentation over 4 spaces
  `<li>Chadcoin for all participating members</li>`
- Line 85: Indentation over 4 spaces
  `<li>XP for both the cabal and individual members</li>`
- Line 86: Indentation over 4 spaces
  `<li>Increased cabal ranking</li>`
- Line 87: Indentation over 4 spaces
  `<li>Chance for rare item drops</li>`
- Line 88: Indentation over 4 spaces
  `</ul>`
- Line 89: Indentation over 4 spaces
  `<p class="text-muted">Even in defeat, participants earn some XP for their effort.</p>`
- Line 90: Indentation over 4 spaces
  `</div>`
- Line 91: Indentation over 4 spaces
  `</div>`
- Line 92: Indentation over 4 spaces
  `</div>`
- Line 98: Indentation over 4 spaces
  `// Set minimum date to today`
- Line 99: Indentation over 4 spaces
  `document.addEventListener('DOMContentLoaded', function() {`
- Line 100: Indentation over 4 spaces
  `const today = new Date();`
- Line 101: Indentation over 4 spaces
  `const formattedDate = today.toISOString().split('T')[0];`
- Line 102: Indentation over 4 spaces
  `document.getElementById('battleDate').setAttribute('min', formattedDate);`
- Line 103: Indentation over 4 spaces
  ``
- Line 104: Indentation over 4 spaces
  `// Set default date to today`
- Line 105: Indentation over 4 spaces
  `document.getElementById('battleDate').value = formattedDate;`
- Line 106: Indentation over 4 spaces
  ``
- Line 107: Indentation over 4 spaces
  `// Set default time to current time + 2 hours`
- Line 108: Indentation over 4 spaces
  `const hours = today.getHours() + 2;`
- Line 109: Indentation over 4 spaces
  `const minutes = today.getMinutes();`
- Line 110: Indentation over 4 spaces
  `const formattedTime = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;`
- Line 111: Indentation over 4 spaces
  `document.getElementById('battleTime').value = formattedTime;`
- Line 112: Indentation over 4 spaces
  `});`

### app\utils\bot_commands.py (628 issues)

#### Code Smells
- Line 118: Explicit commit - check transaction management
  `db.session.commit()`
- Line 136: Explicit commit - check transaction management
  `db.session.commit()`
- Line 149: Explicit commit - check transaction management
  `db.session.commit()`
- Line 164: Explicit commit - check transaction management
  `db.session.commit()`
- Line 176: Explicit commit - check transaction management
  `db.session.commit()`
- Line 184: Explicit commit - check transaction management
  `db.session.commit()`
- Line 245: Explicit commit - check transaction management
  `db.session.commit()`
- Line 414: Explicit commit - check transaction management
  `db.session.commit()`
- Line 424: Explicit commit - check transaction management
  `db.session.commit()`
- Line 75: Catching Exception - too broad
  `except Exception as e:`
- Line 202: Catching Exception - too broad
  `except Exception as e:`
- Line 257: Catching Exception - too broad
  `except Exception as e:`
- Line 305: Catching Exception - too broad
  `except Exception as e:`
- Line 349: Catching Exception - too broad
  `except Exception as e:`
- Line 383: Catching Exception - too broad
  `except Exception as e:`
- Line 428: Catching Exception - too broad
  `except Exception as e:`
- Line 486: Catching Exception - too broad
  `except Exception as e:`
- Line 536: Catching Exception - too broad
  `except Exception as e:`
- Line 584: Catching Exception - too broad
  `except Exception as e:`
- Line 631: Catching Exception - too broad
  `except Exception as e:`
- Line 656: Catching Exception - too broad
  `except Exception as e:`
- Line 523: Datetime usage - check for timezone awareness
  `battle_time = datetime.utcnow() + timedelta(hours=24)`

#### Best Practice Violations
- Line 29: Function without docstring
  `def handle_mention(tweet):`
- Line 79: Function without docstring
  `def handle_create_character(tweet_id, username):`
- Line 208: Function without docstring
  `def handle_fight_request(tweet_id, username, opponent_name):`
- Line 263: Function without docstring
  `def handle_accept_fight(tweet_id, username):`
- Line 311: Function without docstring
  `def handle_check_stats(tweet_id, username):`
- Line 355: Function without docstring
  `def handle_join_cabal(tweet_id, username, cabal_name):`
- Line 387: Function without docstring
  `def handle_create_cabal(tweet_id, username, cabal_name):`
- Line 432: Function without docstring
  `def handle_appoint_officer(tweet_id, username, officer_name, officer_type):`
- Line 490: Function without docstring
  `def handle_schedule_battle(tweet_id, username, opponent_cabal_name):`
- Line 540: Function without docstring
  `def handle_vote_remove_leader(tweet_id, username):`
- Line 588: Function without docstring
  `def handle_opt_in_battle(tweet_id, username):`
- Line 635: Function without docstring
  `def handle_help(tweet_id, username):`
- Line 10: Indentation over 4 spaces
  `get_user_profile, get_user_tweets, analyze_tweets,`
- Line 11: Indentation over 4 spaces
  `calculate_clout, post_reply`
- Line 30: Indentation over 4 spaces
  `"""Process mentions and route to appropriate handler"""`
- Line 31: Indentation over 4 spaces
  `try:`
- Line 32: Indentation over 4 spaces
  `tweet_id = tweet.get('id_str')`
- Line 33: Indentation over 4 spaces
  `user_screen_name = tweet.get('user', {}).get('screen_name')`
- Line 34: Indentation over 4 spaces
  `text = tweet.get('full_text', tweet.get('text', ''))`
- Line 35: Indentation over 4 spaces
  ``
- Line 36: Indentation over 4 spaces
  `# Check which command pattern matches`
- Line 37: Indentation over 4 spaces
  `if CREATE_CHARACTER_PATTERN.search(text):`
- Line 38: Indentation over 4 spaces
  `return handle_create_character(tweet_id, user_screen_name)`
- Line 39: Indentation over 4 spaces
  `elif FIGHT_REQUEST_PATTERN.search(text):`
- Line 40: Indentation over 4 spaces
  `match = FIGHT_REQUEST_PATTERN.search(text)`
- Line 41: Indentation over 4 spaces
  `opponent_name = match.group(1) if match else None`
- Line 42: Indentation over 4 spaces
  `return handle_fight_request(tweet_id, user_screen_name, opponent_name)`
- Line 43: Indentation over 4 spaces
  `elif ACCEPT_FIGHT_PATTERN.search(text):`
- Line 44: Indentation over 4 spaces
  `return handle_accept_fight(tweet_id, user_screen_name)`
- Line 45: Indentation over 4 spaces
  `elif CHECK_STATS_PATTERN.search(text):`
- Line 46: Indentation over 4 spaces
  `return handle_check_stats(tweet_id, user_screen_name)`
- Line 47: Indentation over 4 spaces
  `elif JOIN_CABAL_PATTERN.search(text):`
- Line 48: Indentation over 4 spaces
  `match = JOIN_CABAL_PATTERN.search(text)`
- Line 49: Indentation over 4 spaces
  `cabal_name = match.group(1).strip() if match else None`
- Line 50: Indentation over 4 spaces
  `return handle_join_cabal(tweet_id, user_screen_name, cabal_name)`
- Line 51: Indentation over 4 spaces
  `elif CREATE_CABAL_PATTERN.search(text):`
- Line 52: Indentation over 4 spaces
  `match = CREATE_CABAL_PATTERN.search(text)`
- Line 53: Indentation over 4 spaces
  `cabal_name = match.group(1).strip() if match else None`
- Line 54: Indentation over 4 spaces
  `return handle_create_cabal(tweet_id, user_screen_name, cabal_name)`
- Line 55: Indentation over 4 spaces
  `elif APPOINT_OFFICER_PATTERN.search(text):`
- Line 56: Indentation over 4 spaces
  `match = APPOINT_OFFICER_PATTERN.search(text)`
- Line 57: Indentation over 4 spaces
  `officer_name = match.group(1)`
- Line 58: Indentation over 4 spaces
  `officer_type = match.group(2).lower()`
- Line 59: Indentation over 4 spaces
  `return handle_appoint_officer(tweet_id, user_screen_name, officer_name, officer_type)`
- Line 60: Indentation over 4 spaces
  `elif SCHEDULE_BATTLE_PATTERN.search(text):`
- Line 61: Indentation over 4 spaces
  `match = SCHEDULE_BATTLE_PATTERN.search(text)`
- Line 62: Indentation over 4 spaces
  `opponent_cabal_name = match.group(1).strip() if match else None`
- Line 63: Indentation over 4 spaces
  `return handle_schedule_battle(tweet_id, user_screen_name, opponent_cabal_name)`
- Line 64: Indentation over 4 spaces
  `elif VOTE_REMOVE_LEADER_PATTERN.search(text):`
- Line 65: Indentation over 4 spaces
  `return handle_vote_remove_leader(tweet_id, user_screen_name)`
- Line 66: Indentation over 4 spaces
  `elif OPT_IN_BATTLE_PATTERN.search(text):`
- Line 67: Indentation over 4 spaces
  `return handle_opt_in_battle(tweet_id, user_screen_name)`
- Line 68: Indentation over 4 spaces
  `elif HELP_PATTERN.search(text):`
- Line 69: Indentation over 4 spaces
  `return handle_help(tweet_id, user_screen_name)`
- Line 70: Indentation over 4 spaces
  `else:`
- Line 71: Indentation over 4 spaces
  `# Unknown command`
- Line 72: Indentation over 4 spaces
  `reply = f"@{user_screen_name} I don't understand that command. Try 'HELP @RollMasterChad' for a list of commands."`
- Line 73: Indentation over 4 spaces
  `post_reply(reply, tweet_id)`
- Line 74: Indentation over 4 spaces
  `return False`
- Line 75: Indentation over 4 spaces
  `except Exception as e:`
- Line 76: Indentation over 4 spaces
  `logger.error(f"Error handling mention: {str(e)}")`
- Line 77: Indentation over 4 spaces
  `return False`
- Line 80: Indentation over 4 spaces
  `"""Handle the create character command"""`
- Line 81: Indentation over 4 spaces
  `try:`
- Line 82: Indentation over 4 spaces
  `# Check if user already exists`
- Line 83: Indentation over 4 spaces
  `user = User.query.filter_by(x_username=username).first()`
- Line 84: Indentation over 4 spaces
  `if user and user.chad:`
- Line 85: Indentation over 4 spaces
  `reply = f"@{username} You already have a Chad character! Check your stats with CHECK STATS @RollMasterChad"`
- Line 86: Indentation over 4 spaces
  `post_reply(reply, tweet_id)`
- Line 87: Indentation over 4 spaces
  `return False`
- Line 88: Indentation over 4 spaces
  ``
- Line 89: Indentation over 4 spaces
  `# Get user profile from Twitter`
- Line 90: Indentation over 4 spaces
  `profile = get_user_profile(username)`
- Line 91: Indentation over 4 spaces
  `if not profile:`
- Line 92: Indentation over 4 spaces
  `reply = f"@{username} Failed to fetch your X profile. Please try again later."`
- Line 93: Indentation over 4 spaces
  `post_reply(reply, tweet_id)`
- Line 94: Indentation over 4 spaces
  `return False`
- Line 95: Indentation over 4 spaces
  ``
- Line 96: Indentation over 4 spaces
  `# Get user tweets for analysis`
- Line 97: Indentation over 4 spaces
  `tweets = get_user_tweets(username)`
- Line 98: Indentation over 4 spaces
  `if not tweets:`
- Line 99: Indentation over 4 spaces
  `reply = f"@{username} Couldn't analyze your tweets. Make sure your account is public and try again."`
- Line 100: Indentation over 4 spaces
  `post_reply(reply, tweet_id)`
- Line 101: Indentation over 4 spaces
  `return False`
- Line 102: Indentation over 4 spaces
  ``
- Line 103: Indentation over 4 spaces
  `# Analyze tweets to determine character class and stats`
- Line 104: Indentation over 4 spaces
  `analysis = analyze_tweets(tweets)`
- Line 105: Indentation over 4 spaces
  ``
- Line 106: Indentation over 4 spaces
  `# Create or update User record`
- Line 107: Indentation over 4 spaces
  `if not user:`
- Line 108: Indentation over 4 spaces
  `user = User(`
- Line 109: Indentation over 4 spaces
  `x_id=profile.get('id_str'),`
- Line 110: Indentation over 4 spaces
  `x_username=profile.get('screen_name'),`
- Line 111: Indentation over 4 spaces
  `x_displayname=profile.get('name'),`
- Line 112: Indentation over 4 spaces
  `x_profile_image=profile.get('profile_image_url_https'),`
- Line 113: Indentation over 4 spaces
  `x_followers_count=profile.get('followers_count', 0),`
- Line 114: Indentation over 4 spaces
  `x_following_count=profile.get('friends_count', 0),`
- Line 115: Indentation over 4 spaces
  `last_login=datetime.utcnow()`
- Line 116: Indentation over 4 spaces
  `)`
- Line 117: Indentation over 4 spaces
  `db.session.add(user)`
- Line 118: Indentation over 4 spaces
  `db.session.commit()`
- Line 119: Indentation over 4 spaces
  ``
- Line 120: Indentation over 4 spaces
  `# Calculate Clout stat`
- Line 121: Indentation over 4 spaces
  `clout = calculate_clout(profile.get('id_str'))`
- Line 122: Indentation over 4 spaces
  ``
- Line 123: Indentation over 4 spaces
  `# Get or create Chad Class`
- Line 124: Indentation over 4 spaces
  `chad_class = ChadClass.query.filter_by(name=analysis['chad_class']).first()`
- Line 125: Indentation over 4 spaces
  `if not chad_class:`
- Line 126: Indentation over 4 spaces
  `# Create default class`
- Line 127: Indentation over 4 spaces
  `chad_class = ChadClass(`
- Line 128: Indentation over 4 spaces
  `name=analysis['chad_class'],`
- Line 129: Indentation over 4 spaces
  `description=f"Masters of {analysis['chad_class']} energy",`
- Line 130: Indentation over 4 spaces
  `base_clout_bonus=1,`
- Line 131: Indentation over 4 spaces
  `base_roast_bonus=1,`
- Line 132: Indentation over 4 spaces
  `base_cringe_resistance_bonus=1,`
- Line 133: Indentation over 4 spaces
  `base_drip_bonus=1`
- Line 134: Indentation over 4 spaces
  `)`
- Line 135: Indentation over 4 spaces
  `db.session.add(chad_class)`
- Line 136: Indentation over 4 spaces
  `db.session.commit()`
- Line 137: Indentation over 4 spaces
  ``
- Line 138: Indentation over 4 spaces
  `# Create Chad character`
- Line 139: Indentation over 4 spaces
  `base_stats = analysis['base_stats']`
- Line 140: Indentation over 4 spaces
  `chad = Chad(`
- Line 141: Indentation over 4 spaces
  `user_id=user.id,`
- Line 142: Indentation over 4 spaces
  `class_id=chad_class.id,`
- Line 143: Indentation over 4 spaces
  `clout=clout or base_stats['clout'],`
- Line 144: Indentation over 4 spaces
  `roast_level=base_stats['roast_level'],`
- Line 145: Indentation over 4 spaces
  `cringe_resistance=base_stats['cringe_resistance'],`
- Line 146: Indentation over 4 spaces
  `drip_factor=base_stats['drip_factor']`
- Line 147: Indentation over 4 spaces
  `)`
- Line 148: Indentation over 4 spaces
  `db.session.add(chad)`
- Line 149: Indentation over 4 spaces
  `db.session.commit()`
- Line 150: Indentation over 4 spaces
  ``
- Line 151: Indentation over 4 spaces
  `# Get a starter waifu`
- Line 152: Indentation over 4 spaces
  `starter_waifu_type = WaifuType.query.filter_by(name="Starter Waifu").first()`
- Line 153: Indentation over 4 spaces
  `if not starter_waifu_type:`
- Line 154: Indentation over 4 spaces
  `# Create a default starter waifu type if none exists`
- Line 155: Indentation over 4 spaces
  `starter_rarity = WaifuRarity.query.filter_by(name="Common").first()`
- Line 156: Indentation over 4 spaces
  `if not starter_rarity:`
- Line 157: Indentation over 4 spaces
  `starter_rarity = WaifuRarity(`
- Line 158: Indentation over 4 spaces
  `name="Common",`
- Line 159: Indentation over 4 spaces
  `description="The most common waifu rarity",`
- Line 160: Indentation over 4 spaces
  `base_stat_multiplier=1.0,`
- Line 161: Indentation over 4 spaces
  `drop_rate=0.5`
- Line 162: Indentation over 4 spaces
  `)`
- Line 163: Indentation over 4 spaces
  `db.session.add(starter_rarity)`
- Line 164: Indentation over 4 spaces
  `db.session.commit()`
- Line 165: Indentation over 4 spaces
  ``
- Line 166: Indentation over 4 spaces
  `starter_waifu_type = WaifuType(`
- Line 167: Indentation over 4 spaces
  `name="Starter Waifu",`
- Line 168: Indentation over 4 spaces
  `description="A basic waifu to start your journey",`
- Line 169: Indentation over 4 spaces
  `rarity_id=starter_rarity.id,`
- Line 170: Indentation over 4 spaces
  `base_clout_bonus=1,`
- Line 171: Indentation over 4 spaces
  `base_roast_bonus=1,`
- Line 172: Indentation over 4 spaces
  `base_cringe_resistance_bonus=1,`
- Line 173: Indentation over 4 spaces
  `base_drip_bonus=1`
- Line 174: Indentation over 4 spaces
  `)`
- Line 175: Indentation over 4 spaces
  `db.session.add(starter_waifu_type)`
- Line 176: Indentation over 4 spaces
  `db.session.commit()`
- Line 177: Indentation over 4 spaces
  ``
- Line 178: Indentation over 4 spaces
  `# Create the starter waifu instance`
- Line 179: Indentation over 4 spaces
  `starter_waifu = Waifu(`
- Line 180: Indentation over 4 spaces
  `waifu_type_id=starter_waifu_type.id,`
- Line 181: Indentation over 4 spaces
  `user_id=user.id`
- Line 182: Indentation over 4 spaces
  `)`
- Line 183: Indentation over 4 spaces
  `db.session.add(starter_waifu)`
- Line 184: Indentation over 4 spaces
  `db.session.commit()`
- Line 185: Indentation over 4 spaces
  ``
- Line 186: Indentation over 4 spaces
  `# Equip the starter waifu`
- Line 187: Indentation over 4 spaces
  `starter_waifu.equip(chad)`
- Line 188: Indentation over 4 spaces
  ``
- Line 189: Indentation over 4 spaces
  `# Send a success response`
- Line 190: Indentation over 4 spaces
  `reply = (`
- Line 191: Indentation over 4 spaces
  `f"@{username} Your Chad character has been created! ðŸŽ‰\n\n"`
- Line 192: Indentation over 4 spaces
  `f"Class: {chad_class.name}\n"`
- Line 193: Indentation over 4 spaces
  `f"Clout: {chad.clout}\n"`
- Line 194: Indentation over 4 spaces
  `f"Roast Level: {chad.roast_level}\n"`
- Line 195: Indentation over 4 spaces
  `f"Cringe Resistance: {chad.cringe_resistance}\n"`
- Line 196: Indentation over 4 spaces
  `f"Drip Factor: {chad.drip_factor}\n\n"`
- Line 197: Indentation over 4 spaces
  `f"You received a Starter Waifu! Check your stats with CHECK STATS @RollMasterChad"`
- Line 198: Indentation over 4 spaces
  `)`
- Line 199: Indentation over 4 spaces
  `post_reply(reply, tweet_id)`
- Line 200: Indentation over 4 spaces
  ``
- Line 201: Indentation over 4 spaces
  `return True`
- Line 202: Indentation over 4 spaces
  `except Exception as e:`
- Line 203: Indentation over 4 spaces
  `logger.error(f"Error creating character for {username}: {str(e)}")`
- Line 204: Indentation over 4 spaces
  `reply = f"@{username} You need to create a character first with 'CREATE CHARACTER @RollMasterChad'"`
- Line 205: Indentation over 4 spaces
  `post_reply(reply, tweet_id)`
- Line 206: Indentation over 4 spaces
  `return False`
- Line 209: Indentation over 4 spaces
  `"""Handle a fight request"""`
- Line 210: Indentation over 4 spaces
  `try:`
- Line 211: Indentation over 4 spaces
  `# Check if both users have characters`
- Line 212: Indentation over 4 spaces
  `initiator = User.query.filter_by(x_username=username).first()`
- Line 213: Indentation over 4 spaces
  `opponent = User.query.filter_by(x_username=opponent_name).first()`
- Line 214: Indentation over 4 spaces
  ``
- Line 215: Indentation over 4 spaces
  `if not initiator or not initiator.chad:`
- Line 216: Indentation over 4 spaces
  `reply = f"@{username} You need to create a character first with 'CREATE CHARACTER @RollMasterChad'"`
- Line 217: Indentation over 4 spaces
  `post_reply(reply, tweet_id)`
- Line 218: Indentation over 4 spaces
  `return False`
- Line 219: Indentation over 4 spaces
  ``
- Line 220: Indentation over 4 spaces
  `if not opponent or not opponent.chad:`
- Line 221: Indentation over 4 spaces
  `reply = f"@{username} @{opponent_name} doesn't have a Chad character yet!"`
- Line 222: Indentation over 4 spaces
  `post_reply(reply, tweet_id)`
- Line 223: Indentation over 4 spaces
  `return False`
- Line 224: Indentation over 4 spaces
  ``
- Line 225: Indentation over 4 spaces
  `# Check if there's already a pending battle`
- Line 226: Indentation over 4 spaces
  `existing_battle = Battle.query.filter_by(`
- Line 227: Indentation over 4 spaces
  `initiator_id=initiator.chad.id,`
- Line 228: Indentation over 4 spaces
  `opponent_id=opponent.chad.id,`
- Line 229: Indentation over 4 spaces
  `status='pending'`
- Line 230: Indentation over 4 spaces
  `).first()`
- Line 231: Indentation over 4 spaces
  ``
- Line 232: Indentation over 4 spaces
  `if existing_battle:`
- Line 233: Indentation over 4 spaces
  `reply = f"@{username} You already have a pending battle with @{opponent_name}!"`
- Line 234: Indentation over 4 spaces
  `post_reply(reply, tweet_id)`
- Line 235: Indentation over 4 spaces
  `return False`
- Line 236: Indentation over 4 spaces
  ``
- Line 237: Indentation over 4 spaces
  `# Create a new battle`
- Line 238: Indentation over 4 spaces
  `battle = Battle(`
- Line 239: Indentation over 4 spaces
  `initiator_id=initiator.chad.id,`
- Line 240: Indentation over 4 spaces
  `opponent_id=opponent.chad.id,`
- Line 241: Indentation over 4 spaces
  `status='pending',`
- Line 242: Indentation over 4 spaces
  `challenge_tweet_id=tweet_id`
- Line 243: Indentation over 4 spaces
  `)`
- Line 244: Indentation over 4 spaces
  `db.session.add(battle)`
- Line 245: Indentation over 4 spaces
  `db.session.commit()`
- Line 246: Indentation over 4 spaces
  ``
- Line 247: Indentation over 4 spaces
  `# Send a challenge response`
- Line 248: Indentation over 4 spaces
  `reply = (`
- Line 249: Indentation over 4 spaces
  `f"🔥 BATTLE CHALLENGE! 🔥\n\n"`
- Line 250: Indentation over 4 spaces
  `f"@{opponent_name}, @{username} is challenging you to a Chad Battle!\n\n"`
- Line 251: Indentation over 4 spaces
  `f"Reply with 'ACCEPT BATTLE @RollMasterChad' to fight or ignore to decline.\n"`
- Line 252: Indentation over 4 spaces
  `f"The winner might claim one of the loser's waifus as a prize!"`
- Line 253: Indentation over 4 spaces
  `)`
- Line 254: Indentation over 4 spaces
  `post_reply(reply, tweet_id)`
- Line 255: Indentation over 4 spaces
  ``
- Line 256: Indentation over 4 spaces
  `return True`
- Line 257: Indentation over 4 spaces
  `except Exception as e:`
- Line 258: Indentation over 4 spaces
  `logger.error(f"Error handling fight request from {username} to {opponent_name}: {str(e)}")`
- Line 259: Indentation over 4 spaces
  `reply = f"@{username} Sorry, there was an error processing your battle challenge. Please try again later."`
- Line 260: Indentation over 4 spaces
  `post_reply(reply, tweet_id)`
- Line 261: Indentation over 4 spaces
  `return False`
- Line 264: Indentation over 4 spaces
  `"""Handle accepting a fight"""`
- Line 265: Indentation over 4 spaces
  `try:`
- Line 266: Indentation over 4 spaces
  `# Get the user`
- Line 267: Indentation over 4 spaces
  `user = User.query.filter_by(x_username=username).first()`
- Line 268: Indentation over 4 spaces
  `if not user or not user.chad:`
- Line 269: Indentation over 4 spaces
  `reply = f"@{username} You need to create a character first with 'CREATE CHARACTER @RollMasterChad'"`
- Line 270: Indentation over 4 spaces
  `post_reply(reply, tweet_id)`
- Line 271: Indentation over 4 spaces
  `return False`
- Line 272: Indentation over 4 spaces
  ``
- Line 273: Indentation over 4 spaces
  `# Find pending battles where this user is the opponent`
- Line 274: Indentation over 4 spaces
  `pending_battle = Battle.query.filter_by(`
- Line 275: Indentation over 4 spaces
  `opponent_id=user.chad.id,`
- Line 276: Indentation over 4 spaces
  `status='pending'`
- Line 277: Indentation over 4 spaces
  `).order_by(Battle.created_at.desc()).first()`
- Line 278: Indentation over 4 spaces
  ``
- Line 279: Indentation over 4 spaces
  `if not pending_battle:`
- Line 280: Indentation over 4 spaces
  `reply = f"@{username} You don't have any pending battle challenges!"`
- Line 281: Indentation over 4 spaces
  `post_reply(reply, tweet_id)`
- Line 282: Indentation over 4 spaces
  `return False`
- Line 283: Indentation over 4 spaces
  ``
- Line 284: Indentation over 4 spaces
  `# Accept the battle`
- Line 285: Indentation over 4 spaces
  `success, message = pending_battle.accept(tweet_id)`
- Line 286: Indentation over 4 spaces
  `if not success:`
- Line 287: Indentation over 4 spaces
  `reply = f"@{username} {message}"`
- Line 288: Indentation over 4 spaces
  `post_reply(reply, tweet_id)`
- Line 289: Indentation over 4 spaces
  `return False`
- Line 290: Indentation over 4 spaces
  ``
- Line 291: Indentation over 4 spaces
  `# Simulate the battle`
- Line 292: Indentation over 4 spaces
  `success, result = pending_battle.simulate()`
- Line 293: Indentation over 4 spaces
  `if not success:`
- Line 294: Indentation over 4 spaces
  `reply = f"@{username} {result}"`
- Line 295: Indentation over 4 spaces
  `post_reply(reply, tweet_id)`
- Line 296: Indentation over 4 spaces
  `return False`
- Line 297: Indentation over 4 spaces
  ``
- Line 298: Indentation over 4 spaces
  `# Get the battle summary`
- Line 299: Indentation over 4 spaces
  `summary = pending_battle.get_battle_summary()`
- Line 300: Indentation over 4 spaces
  ``
- Line 301: Indentation over 4 spaces
  `# Send the battle results`
- Line 302: Indentation over 4 spaces
  `post_reply(summary, tweet_id)`
- Line 303: Indentation over 4 spaces
  ``
- Line 304: Indentation over 4 spaces
  `return True`
- Line 305: Indentation over 4 spaces
  `except Exception as e:`
- Line 306: Indentation over 4 spaces
  `logger.error(f"Error handling fight acceptance from {username}: {str(e)}")`
- Line 307: Indentation over 4 spaces
  `reply = f"@{username} Sorry, there was an error processing the battle. Please try again later."`
- Line 308: Indentation over 4 spaces
  `post_reply(reply, tweet_id)`
- Line 309: Indentation over 4 spaces
  `return False`
- Line 312: Indentation over 4 spaces
  `"""Handle stats check request"""`
- Line 313: Indentation over 4 spaces
  `try:`
- Line 314: Indentation over 4 spaces
  `user = User.query.filter_by(x_username=username).first()`
- Line 315: Indentation over 4 spaces
  `if not user or not user.chad:`
- Line 316: Indentation over 4 spaces
  `reply = f"@{username} You need to create a character first with 'CREATE CHARACTER @RollMasterChad'"`
- Line 317: Indentation over 4 spaces
  `post_reply(reply, tweet_id)`
- Line 318: Indentation over 4 spaces
  `return False`
- Line 319: Indentation over 4 spaces
  ``
- Line 320: Indentation over 4 spaces
  `chad = user.chad`
- Line 321: Indentation over 4 spaces
  `stats = chad.calculate_stats()`
- Line 322: Indentation over 4 spaces
  ``
- Line 323: Indentation over 4 spaces
  `# Get equipped waifus`
- Line 324: Indentation over 4 spaces
  `equipped_waifus = chad.equipped_waifus.all()`
- Line 325: Indentation over 4 spaces
  `waifu_names = [w.waifu_type.name for w in equipped_waifus]`
- Line 326: Indentation over 4 spaces
  ``
- Line 327: Indentation over 4 spaces
  `# Create stats message`
- Line 328: Indentation over 4 spaces
  `reply = (`
- Line 329: Indentation over 4 spaces
  `f"@{username} Your Chad Stats:\n\n"`
- Line 330: Indentation over 4 spaces
  `f"Class: {chad.chad_class.name}\n"`
- Line 331: Indentation over 4 spaces
  `f"Level: {chad.level}\n"`
- Line 332: Indentation over 4 spaces
  `f"Clout: {stats['clout']}\n"`
- Line 333: Indentation over 4 spaces
  `f"Roast Level: {stats['roast_level']}\n"`
- Line 334: Indentation over 4 spaces
  `f"Cringe Resistance: {stats['cringe_resistance']}\n"`
- Line 335: Indentation over 4 spaces
  `f"Drip Factor: {stats['drip_factor']}\n\n"`
- Line 336: Indentation over 4 spaces
  `f"Battles Won: {chad.battles_won}\n"`
- Line 337: Indentation over 4 spaces
  `f"Battles Lost: {chad.battles_lost}\n"`
- Line 338: Indentation over 4 spaces
  `)`
- Line 339: Indentation over 4 spaces
  ``
- Line 340: Indentation over 4 spaces
  `if waifu_names:`
- Line 341: Indentation over 4 spaces
  `reply += f"\nEquipped Waifus: {', '.join(waifu_names)}"`
- Line 342: Indentation over 4 spaces
  ``
- Line 343: Indentation over 4 spaces
  `if chad.cabal_membership and chad.cabal_membership.cabal:`
- Line 344: Indentation over 4 spaces
  `cabal = chad.cabal_membership.cabal`
- Line 345: Indentation over 4 spaces
  `reply += f"\n\nCabal: {cabal.name} (Level {cabal.level})"`
- Line 346: Indentation over 4 spaces
  ``
- Line 347: Indentation over 4 spaces
  `post_reply(reply, tweet_id)`
- Line 348: Indentation over 4 spaces
  `return True`
- Line 349: Indentation over 4 spaces
  `except Exception as e:`
- Line 350: Indentation over 4 spaces
  `logger.error(f"Error checking stats for {username}: {str(e)}")`
- Line 351: Indentation over 4 spaces
  `reply = f"@{username} Sorry, there was an error checking your stats. Please try again later."`
- Line 352: Indentation over 4 spaces
  `post_reply(reply, tweet_id)`
- Line 353: Indentation over 4 spaces
  `return False`
- Line 356: Indentation over 4 spaces
  `"""Handle join cabal request"""`
- Line 357: Indentation over 4 spaces
  `try:`
- Line 358: Indentation over 4 spaces
  `# Get user by twitter handle`
- Line 359: Indentation over 4 spaces
  `from app.models.cabal import Cabal`
- Line 360: Indentation over 4 spaces
  `from app.models.user import User`
- Line 361: Indentation over 4 spaces
  ``
- Line 362: Indentation over 4 spaces
  `user = User.query.filter_by(twitter_handle=username).first()`
- Line 363: Indentation over 4 spaces
  ``
- Line 364: Indentation over 4 spaces
  `if not user or not user.chad:`
- Line 365: Indentation over 4 spaces
  `return f"@{username} You need to create a character first. Use CREATE CHARACTER @RollMasterChad to get started."`
- Line 366: Indentation over 4 spaces
  ``
- Line 367: Indentation over 4 spaces
  `# Check if user is already in a cabal`
- Line 368: Indentation over 4 spaces
  `if user.chad.cabal_membership:`
- Line 369: Indentation over 4 spaces
  `return f"@{username} You're already in the cabal '{user.chad.cabal_membership.cabal.name}'! Leave your current cabal first."`
- Line 370: Indentation over 4 spaces
  ``
- Line 371: Indentation over 4 spaces
  `# Find the cabal`
- Line 372: Indentation over 4 spaces
  `cabal = Cabal.query.filter_by(name=cabal_name).first()`
- Line 373: Indentation over 4 spaces
  `if not cabal:`
- Line 374: Indentation over 4 spaces
  `return f"@{username} The cabal '{cabal_name}' doesn't exist. Create it with CREATE NEW CABAL name @RollMasterChad"`
- Line 375: Indentation over 4 spaces
  ``
- Line 376: Indentation over 4 spaces
  `# Try to join the cabal`
- Line 377: Indentation over 4 spaces
  `success, message = cabal.add_member(user.chad.id)`
- Line 378: Indentation over 4 spaces
  ``
- Line 379: Indentation over 4 spaces
  `if success:`
- Line 380: Indentation over 4 spaces
  `return f"@{username} You have successfully joined the cabal '{cabal_name}'!"`
- Line 381: Indentation over 4 spaces
  `else:`
- Line 382: Indentation over 4 spaces
  `return f"@{username} Unable to join cabal: {message}"`
- Line 383: Indentation over 4 spaces
  `except Exception as e:`
- Line 384: Indentation over 4 spaces
  `logger.error(f"Error handling join cabal request from {username}: {str(e)}")`
- Line 385: Indentation over 4 spaces
  `return f"@{username} Sorry, there was an error joining the cabal. Please try again later."`
- Line 388: Indentation over 4 spaces
  `"""Handle create cabal request"""`
- Line 389: Indentation over 4 spaces
  `try:`
- Line 390: Indentation over 4 spaces
  `from app.models.cabal import Cabal`
- Line 391: Indentation over 4 spaces
  `from app.models.user import User`
- Line 392: Indentation over 4 spaces
  ``
- Line 393: Indentation over 4 spaces
  `user = User.query.filter_by(twitter_handle=username).first()`
- Line 394: Indentation over 4 spaces
  ``
- Line 395: Indentation over 4 spaces
  `if not user or not user.chad:`
- Line 396: Indentation over 4 spaces
  `return f"@{username} You need to create a character first. Use CREATE CHARACTER @RollMasterChad to get started."`
- Line 397: Indentation over 4 spaces
  ``
- Line 398: Indentation over 4 spaces
  `# Check if user is already in a cabal`
- Line 399: Indentation over 4 spaces
  `if user.chad.cabal_membership:`
- Line 400: Indentation over 4 spaces
  `return f"@{username} You're already in the cabal '{user.chad.cabal_membership.cabal.name}'! Leave your current cabal first."`
- Line 401: Indentation over 4 spaces
  ``
- Line 402: Indentation over 4 spaces
  `# Check if the cabal name already exists`
- Line 403: Indentation over 4 spaces
  `existing_cabal = Cabal.query.filter_by(name=cabal_name).first()`
- Line 404: Indentation over 4 spaces
  `if existing_cabal:`
- Line 405: Indentation over 4 spaces
  `return f"@{username} The cabal '{cabal_name}' already exists! Try joining it with JOIN CABAL name @RollMasterChad"`
- Line 406: Indentation over 4 spaces
  ``
- Line 407: Indentation over 4 spaces
  `# Create the cabal`
- Line 408: Indentation over 4 spaces
  `cabal = Cabal(`
- Line 409: Indentation over 4 spaces
  `name=cabal_name,`
- Line 410: Indentation over 4 spaces
  `description=f"Cabal led by {username}",`
- Line 411: Indentation over 4 spaces
  `leader_id=user.chad.id`
- Line 412: Indentation over 4 spaces
  `)`
- Line 413: Indentation over 4 spaces
  `db.session.add(cabal)`
- Line 414: Indentation over 4 spaces
  `db.session.commit()`
- Line 415: Indentation over 4 spaces
  ``
- Line 416: Indentation over 4 spaces
  `# Add user as member`
- Line 417: Indentation over 4 spaces
  `from app.models.cabal import CabalMember`
- Line 418: Indentation over 4 spaces
  `member = CabalMember(`
- Line 419: Indentation over 4 spaces
  `cabal_id=cabal.id,`
- Line 420: Indentation over 4 spaces
  `chad_id=user.chad.id,`
- Line 421: Indentation over 4 spaces
  `is_active=True`
- Line 422: Indentation over 4 spaces
  `)`
- Line 423: Indentation over 4 spaces
  `db.session.add(member)`
- Line 424: Indentation over 4 spaces
  `db.session.commit()`
- Line 425: Indentation over 4 spaces
  ``
- Line 426: Indentation over 4 spaces
  `return f"@{username} Successfully created cabal '{cabal_name}'! Invite others to join with JOIN CABAL name @RollMasterChad"`
- Line 427: Indentation over 4 spaces
  ``
- Line 428: Indentation over 4 spaces
  `except Exception as e:`
- Line 429: Indentation over 4 spaces
  `logger.error(f"Error creating cabal for {username}: {str(e)}")`
- Line 430: Indentation over 4 spaces
  `return f"@{username} Sorry, there was an error creating the cabal. Please try again later."`
- Line 433: Indentation over 4 spaces
  `"""Handle appointing a cabal officer"""`
- Line 434: Indentation over 4 spaces
  `try:`
- Line 435: Indentation over 4 spaces
  `from app.models.cabal import Cabal, CabalMember`
- Line 436: Indentation over 4 spaces
  `from app.models.user import User`
- Line 437: Indentation over 4 spaces
  ``
- Line 438: Indentation over 4 spaces
  `# Map the officer type from the tweet to the database role type`
- Line 439: Indentation over 4 spaces
  `role_type_map = {`
- Line 440: Indentation over 4 spaces
  `'clout': 'clout',`
- Line 441: Indentation over 4 spaces
  `'roast': 'roast_level',`
- Line 442: Indentation over 4 spaces
  `'cringe': 'cringe_resistance',`
- Line 443: Indentation over 4 spaces
  `'drip': 'drip_factor'`
- Line 444: Indentation over 4 spaces
  `}`
- Line 445: Indentation over 4 spaces
  ``
- Line 446: Indentation over 4 spaces
  `# Convert the officer type to the correct database role type`
- Line 447: Indentation over 4 spaces
  `role_type = role_type_map.get(officer_type.lower())`
- Line 448: Indentation over 4 spaces
  `if not role_type:`
- Line 449: Indentation over 4 spaces
  `return f"@{username} Invalid officer type. Must be CLOUT, ROAST, CRINGE, or DRIP."`
- Line 450: Indentation over 4 spaces
  ``
- Line 451: Indentation over 4 spaces
  `# Get the appointer (cabal leader)`
- Line 452: Indentation over 4 spaces
  `leader_user = User.query.filter_by(twitter_handle=username).first()`
- Line 453: Indentation over 4 spaces
  ``
- Line 454: Indentation over 4 spaces
  `if not leader_user or not leader_user.chad:`
- Line 455: Indentation over 4 spaces
  `return f"@{username} You need to create a character first. Use CREATE CHARACTER @RollMasterChad to get started."`
- Line 456: Indentation over 4 spaces
  ``
- Line 457: Indentation over 4 spaces
  `# Check if user is a cabal leader`
- Line 458: Indentation over 4 spaces
  `cabal = Cabal.query.filter_by(leader_id=leader_user.chad.id).first()`
- Line 459: Indentation over 4 spaces
  ``
- Line 460: Indentation over 4 spaces
  `if not cabal:`
- Line 461: Indentation over 4 spaces
  `return f"@{username} You are not the Lord of the Shill for any cabal."`
- Line 462: Indentation over 4 spaces
  ``
- Line 463: Indentation over 4 spaces
  `# Find the officer user`
- Line 464: Indentation over 4 spaces
  `officer_user = User.query.filter_by(twitter_handle=officer_name).first()`
- Line 465: Indentation over 4 spaces
  ``
- Line 466: Indentation over 4 spaces
  `if not officer_user or not officer_user.chad:`
- Line 467: Indentation over 4 spaces
  `return f"@{username} The user @{officer_name} does not have a character in the game."`
- Line 468: Indentation over 4 spaces
  ``
- Line 469: Indentation over 4 spaces
  `# Check if the officer is in the leader's cabal`
- Line 470: Indentation over 4 spaces
  `member = CabalMember.query.filter_by(`
- Line 471: Indentation over 4 spaces
  `cabal_id=cabal.id,`
- Line 472: Indentation over 4 spaces
  `chad_id=officer_user.chad.id`
- Line 473: Indentation over 4 spaces
  `).first()`
- Line 474: Indentation over 4 spaces
  ``
- Line 475: Indentation over 4 spaces
  `if not member:`
- Line 476: Indentation over 4 spaces
  `return f"@{username} @{officer_name} is not a member of your cabal."`
- Line 477: Indentation over 4 spaces
  ``
- Line 478: Indentation over 4 spaces
  `# Appoint the officer`
- Line 479: Indentation over 4 spaces
  `success, message = cabal.appoint_officer(officer_user.chad.id, role_type)`
- Line 480: Indentation over 4 spaces
  ``
- Line 481: Indentation over 4 spaces
  `if success:`
- Line 482: Indentation over 4 spaces
  `officer_title = cabal.get_officer_title(role_type)`
- Line 483: Indentation over 4 spaces
  `return f"@{username} @{officer_name} has been appointed as {officer_title} of your cabal."`
- Line 484: Indentation over 4 spaces
  `else:`
- Line 485: Indentation over 4 spaces
  `return f"@{username} Unable to appoint officer: {message}"`
- Line 486: Indentation over 4 spaces
  `except Exception as e:`
- Line 487: Indentation over 4 spaces
  `logger.error(f"Error appointing officer from {username}: {str(e)}")`
- Line 488: Indentation over 4 spaces
  `return f"@{username} Sorry, there was an error appointing the officer. Please try again later."`
- Line 491: Indentation over 4 spaces
  `"""Handle scheduling a cabal battle"""`
- Line 492: Indentation over 4 spaces
  `try:`
- Line 493: Indentation over 4 spaces
  `from app.models.cabal import Cabal`
- Line 494: Indentation over 4 spaces
  `from app.models.user import User`
- Line 495: Indentation over 4 spaces
  ``
- Line 496: Indentation over 4 spaces
  `# Get the cabal leader`
- Line 497: Indentation over 4 spaces
  `leader_user = User.query.filter_by(twitter_handle=username).first()`
- Line 498: Indentation over 4 spaces
  ``
- Line 499: Indentation over 4 spaces
  `if not leader_user or not leader_user.chad:`
- Line 500: Indentation over 4 spaces
  `return f"@{username} You need to create a character first. Use CREATE CHARACTER @RollMasterChad to get started."`
- Line 501: Indentation over 4 spaces
  ``
- Line 502: Indentation over 4 spaces
  `# Check if user is a cabal leader`
- Line 503: Indentation over 4 spaces
  `cabal = Cabal.query.filter_by(leader_id=leader_user.chad.id).first()`
- Line 504: Indentation over 4 spaces
  ``
- Line 505: Indentation over 4 spaces
  `if not cabal:`
- Line 506: Indentation over 4 spaces
  `return f"@{username} You are not the Lord of the Shill for any cabal."`
- Line 507: Indentation over 4 spaces
  ``
- Line 508: Indentation over 4 spaces
  `# Find the opponent cabal`
- Line 509: Indentation over 4 spaces
  `opponent_cabal = Cabal.query.filter_by(name=opponent_cabal_name).first()`
- Line 510: Indentation over 4 spaces
  ``
- Line 511: Indentation over 4 spaces
  `if not opponent_cabal:`
- Line 512: Indentation over 4 spaces
  `return f"@{username} The cabal '{opponent_cabal_name}' does not exist."`
- Line 513: Indentation over 4 spaces
  ``
- Line 514: Indentation over 4 spaces
  `# Check if this is our own cabal`
- Line 515: Indentation over 4 spaces
  `if cabal.id == opponent_cabal.id:`
- Line 516: Indentation over 4 spaces
  `return f"@{username} You cannot battle your own cabal."`
- Line 517: Indentation over 4 spaces
  ``
- Line 518: Indentation over 4 spaces
  `# Check if we can schedule more battles this week`
- Line 519: Indentation over 4 spaces
  `if not cabal.can_schedule_battle():`
- Line 520: Indentation over 4 spaces
  `return f"@{username} Your cabal has already scheduled the maximum 3 battles this week."`
- Line 521: Indentation over 4 spaces
  ``
- Line 522: Indentation over 4 spaces
  `# Schedule the battle for 24 hours from now`
- Line 523: Indentation over 4 spaces
  `battle_time = datetime.utcnow() + timedelta(hours=24)`
- Line 524: Indentation over 4 spaces
  `success, message = cabal.schedule_battle(opponent_cabal.id, battle_time)`
- Line 525: Indentation over 4 spaces
  ``
- Line 526: Indentation over 4 spaces
  `if success:`
- Line 527: Indentation over 4 spaces
  `# Get opponent cabal leader for the mention`
- Line 528: Indentation over 4 spaces
  `from app.models.chad import Chad`
- Line 529: Indentation over 4 spaces
  `opponent_leader = Chad.query.get(opponent_cabal.leader_id)`
- Line 530: Indentation over 4 spaces
  `opponent_user = User.query.filter_by(chad_id=opponent_leader.id).first()`
- Line 531: Indentation over 4 spaces
  `opponent_username = opponent_user.twitter_handle if opponent_user else "Unknown"`
- Line 532: Indentation over 4 spaces
  ``
- Line 533: Indentation over 4 spaces
  `return f"@{username} Battle with '{opponent_cabal_name}' scheduled! @{opponent_username} your cabal has been challenged to battle in 24 hours. Members can opt in with JOIN NEXT CABAL BATTLE @RollMasterChad"`
- Line 534: Indentation over 4 spaces
  `else:`
- Line 535: Indentation over 4 spaces
  `return f"@{username} Unable to schedule battle: {message}"`
- Line 536: Indentation over 4 spaces
  `except Exception as e:`
- Line 537: Indentation over 4 spaces
  `logger.error(f"Error scheduling battle from {username}: {str(e)}")`
- Line 538: Indentation over 4 spaces
  `return f"@{username} Sorry, there was an error scheduling the battle. Please try again later."`
- Line 541: Indentation over 4 spaces
  `"""Handle voting to remove a cabal leader"""`
- Line 542: Indentation over 4 spaces
  `try:`
- Line 543: Indentation over 4 spaces
  `from app.models.cabal import CabalMember`
- Line 544: Indentation over 4 spaces
  `from app.models.user import User`
- Line 545: Indentation over 4 spaces
  ``
- Line 546: Indentation over 4 spaces
  `# Get the voter`
- Line 547: Indentation over 4 spaces
  `voter_user = User.query.filter_by(twitter_handle=username).first()`
- Line 548: Indentation over 4 spaces
  ``
- Line 549: Indentation over 4 spaces
  `if not voter_user or not voter_user.chad:`
- Line 550: Indentation over 4 spaces
  `return f"@{username} You need to create a character first. Use CREATE CHARACTER @RollMasterChad to get started."`
- Line 551: Indentation over 4 spaces
  ``
- Line 552: Indentation over 4 spaces
  `# Check if voter is in a cabal`
- Line 553: Indentation over 4 spaces
  `cabal_member = CabalMember.query.filter_by(chad_id=voter_user.chad.id).first()`
- Line 554: Indentation over 4 spaces
  ``
- Line 555: Indentation over 4 spaces
  `if not cabal_member:`
- Line 556: Indentation over 4 spaces
  `return f"@{username} You are not a member of any cabal."`
- Line 557: Indentation over 4 spaces
  ``
- Line 558: Indentation over 4 spaces
  `# Check if voter is the leader (can't vote against themselves)`
- Line 559: Indentation over 4 spaces
  `if cabal_member.cabal.leader_id == voter_user.chad.id:`
- Line 560: Indentation over 4 spaces
  `return f"@{username} You cannot vote to remove yourself as leader."`
- Line 561: Indentation over 4 spaces
  ``
- Line 562: Indentation over 4 spaces
  `# Cast the vote`
- Line 563: Indentation over 4 spaces
  `success, message = cabal_member.cabal.vote_to_remove_leader(voter_user.chad.id)`
- Line 564: Indentation over 4 spaces
  ``
- Line 565: Indentation over 4 spaces
  `if success:`
- Line 566: Indentation over 4 spaces
  `# If the message indicates the leader was removed, a new leader was appointed`
- Line 567: Indentation over 4 spaces
  `if "is now the leader" in message:`
- Line 568: Indentation over 4 spaces
  `return f"@{username} Your vote was successful! {message}"`
- Line 569: Indentation over 4 spaces
  `else:`
- Line 570: Indentation over 4 spaces
  `# Get current vote count and percentage`
- Line 571: Indentation over 4 spaces
  `from app.models.cabal import CabalVote`
- Line 572: Indentation over 4 spaces
  `votes = CabalVote.query.filter_by(`
- Line 573: Indentation over 4 spaces
  `cabal_id=cabal_member.cabal.id,`
- Line 574: Indentation over 4 spaces
  `vote_type='remove_leader',`
- Line 575: Indentation over 4 spaces
  `target_id=cabal_member.cabal.leader_id`
- Line 576: Indentation over 4 spaces
  `).count()`
- Line 577: Indentation over 4 spaces
  ``
- Line 578: Indentation over 4 spaces
  `active_members = cabal_member.cabal.get_active_member_count()`
- Line 579: Indentation over 4 spaces
  `percentage = (votes / active_members * 100) if active_members > 0 else 0`
- Line 580: Indentation over 4 spaces
  ``
- Line 581: Indentation over 4 spaces
  `return f"@{username} Your vote to remove the cabal leader has been recorded. Current status: {votes} votes ({percentage:.1f}% of active members)."`
- Line 582: Indentation over 4 spaces
  `else:`
- Line 583: Indentation over 4 spaces
  `return f"@{username} Unable to vote: {message}"`
- Line 584: Indentation over 4 spaces
  `except Exception as e:`
- Line 585: Indentation over 4 spaces
  `logger.error(f"Error processing vote from {username}: {str(e)}")`
- Line 586: Indentation over 4 spaces
  `return f"@{username} Sorry, there was an error processing your vote. Please try again later."`
- Line 589: Indentation over 4 spaces
  `"""Handle opting into a cabal battle"""`
- Line 590: Indentation over 4 spaces
  `try:`
- Line 591: Indentation over 4 spaces
  `from app.models.cabal import CabalMember, CabalBattle`
- Line 592: Indentation over 4 spaces
  `from app.models.user import User`
- Line 593: Indentation over 4 spaces
  ``
- Line 594: Indentation over 4 spaces
  `# Get the user`
- Line 595: Indentation over 4 spaces
  `user = User.query.filter_by(twitter_handle=username).first()`
- Line 596: Indentation over 4 spaces
  ``
- Line 597: Indentation over 4 spaces
  `if not user or not user.chad:`
- Line 598: Indentation over 4 spaces
  `return f"@{username} You need to create a character first. Use CREATE CHARACTER @RollMasterChad to get started."`
- Line 599: Indentation over 4 spaces
  ``
- Line 600: Indentation over 4 spaces
  `# Check if user is in a cabal`
- Line 601: Indentation over 4 spaces
  `cabal_member = CabalMember.query.filter_by(chad_id=user.chad.id).first()`
- Line 602: Indentation over 4 spaces
  ``
- Line 603: Indentation over 4 spaces
  `if not cabal_member:`
- Line 604: Indentation over 4 spaces
  `return f"@{username} You are not a member of any cabal."`
- Line 605: Indentation over 4 spaces
  ``
- Line 606: Indentation over 4 spaces
  `# Find the next scheduled battle for this cabal`
- Line 607: Indentation over 4 spaces
  `next_battle = CabalBattle.query.filter_by(`
- Line 608: Indentation over 4 spaces
  `cabal_id=cabal_member.cabal.id,`
- Line 609: Indentation over 4 spaces
  `completed=False`
- Line 610: Indentation over 4 spaces
  `).filter(`
- Line 611: Indentation over 4 spaces
  `CabalBattle.scheduled_at > datetime.utcnow()`
- Line 612: Indentation over 4 spaces
  `).order_by(CabalBattle.scheduled_at).first()`
- Line 613: Indentation over 4 spaces
  ``
- Line 614: Indentation over 4 spaces
  `if not next_battle:`
- Line 615: Indentation over 4 spaces
  `return f"@{username} Your cabal does not have any upcoming battles scheduled."`
- Line 616: Indentation over 4 spaces
  ``
- Line 617: Indentation over 4 spaces
  `# Opt into the battle`
- Line 618: Indentation over 4 spaces
  `success, message = cabal_member.opt_into_battle(next_battle.id)`
- Line 619: Indentation over 4 spaces
  ``
- Line 620: Indentation over 4 spaces
  `if success:`
- Line 621: Indentation over 4 spaces
  `# Get opponent cabal name`
- Line 622: Indentation over 4 spaces
  `from app.models.cabal import Cabal`
- Line 623: Indentation over 4 spaces
  `opponent_cabal = Cabal.query.get(next_battle.opponent_cabal_id)`
- Line 624: Indentation over 4 spaces
  `opponent_name = opponent_cabal.name if opponent_cabal else "Unknown"`
- Line 625: Indentation over 4 spaces
  ``
- Line 626: Indentation over 4 spaces
  `battle_time = next_battle.scheduled_at.strftime("%Y-%m-%d %H:%M UTC")`
- Line 627: Indentation over 4 spaces
  ``
- Line 628: Indentation over 4 spaces
  `return f"@{username} You have successfully opted into the battle against '{opponent_name}' scheduled for {battle_time}. Prepare for glory!"`
- Line 629: Indentation over 4 spaces
  `else:`
- Line 630: Indentation over 4 spaces
  `return f"@{username} Unable to opt into battle: {message}"`
- Line 631: Indentation over 4 spaces
  `except Exception as e:`
- Line 632: Indentation over 4 spaces
  `logger.error(f"Error opting into battle from {username}: {str(e)}")`
- Line 633: Indentation over 4 spaces
  `return f"@{username} Sorry, there was an error opting into the battle. Please try again later."`
- Line 636: Indentation over 4 spaces
  `"""Handle help request"""`
- Line 637: Indentation over 4 spaces
  `try:`
- Line 638: Indentation over 4 spaces
  `help_message = f"""@{username} Chad Battles Commands:`
- Line 654: Indentation over 4 spaces
  ``
- Line 655: Indentation over 4 spaces
  `return help_message`
- Line 656: Indentation over 4 spaces
  `except Exception as e:`
- Line 657: Indentation over 4 spaces
  `logger.error(f"Error generating help for {username}: {str(e)}")`
- Line 658: Indentation over 4 spaces
  `return f"@{username} Sorry, there was an error generating help. Please try again later."`

### tests\test_cabal_mock.py (150 issues)

#### Best Practice Violations
- Line 7: Function without docstring
  `def setUp(self):`
- Line 25: Function without docstring
  `def mock_add_member(chad_id):`
- Line 35: Function without docstring
  `def mock_remove_member(chad_id):`
- Line 53: Function without docstring
  `def mock_appoint_officer(chad_id, role):`
- Line 73: Function without docstring
  `def mock_get_officer(role):`
- Line 78: Function without docstring
  `def test_cabal_creation(self):`
- Line 89: Function without docstring
  `def test_add_member(self):`
- Line 106: Function without docstring
  `def test_remove_member(self):`
- Line 122: Function without docstring
  `def test_appoint_officer(self):`
- Line 15: Self assignment in method/constructor
  `self.mock_cabal.id = self.cabal_id`
- Line 18: Self assignment in method/constructor
  `self.mock_cabal.leader_id = self.test_chad_ids[0]`
- Line 29: Self assignment in method/constructor
  `self.mock_cabal.member_count = len(self.mock_members)`
- Line 41: Self assignment in method/constructor
  `self.mock_cabal.member_count = len(self.mock_members)`
- Line 7: Indentation over 4 spaces
  `def setUp(self):`
- Line 8: Indentation over 4 spaces
  `"""Set up test environment before each test"""`
- Line 9: Indentation over 4 spaces
  `# Create mock IDs for testing`
- Line 10: Indentation over 4 spaces
  `self.test_chad_ids = [str(uuid.uuid4()) for _ in range(5)]`
- Line 11: Indentation over 4 spaces
  `self.cabal_id = str(uuid.uuid4())`
- Line 12: Indentation over 4 spaces
  ``
- Line 13: Indentation over 4 spaces
  `# Create a mock cabal class`
- Line 14: Indentation over 4 spaces
  `self.mock_cabal = MagicMock()`
- Line 15: Indentation over 4 spaces
  `self.mock_cabal.id = self.cabal_id`
- Line 16: Indentation over 4 spaces
  `self.mock_cabal.name = "Test Cabal"`
- Line 17: Indentation over 4 spaces
  `self.mock_cabal.description = "A test cabal"`
- Line 18: Indentation over 4 spaces
  `self.mock_cabal.leader_id = self.test_chad_ids[0]`
- Line 19: Indentation over 4 spaces
  `self.mock_cabal.level = 1`
- Line 20: Indentation over 4 spaces
  `self.mock_cabal.xp = 0`
- Line 21: Indentation over 4 spaces
  `self.mock_cabal.invite_code = "ABC123"`
- Line 22: Indentation over 4 spaces
  `self.mock_cabal.member_count = 0`
- Line 23: Indentation over 4 spaces
  ``
- Line 24: Indentation over 4 spaces
  `# Mock the add_member method`
- Line 25: Indentation over 4 spaces
  `def mock_add_member(chad_id):`
- Line 26: Indentation over 4 spaces
  `if chad_id in self.mock_members:`
- Line 27: Indentation over 4 spaces
  `return False, "Member already in cabal"`
- Line 28: Indentation over 4 spaces
  `self.mock_members.append(chad_id)`
- Line 29: Indentation over 4 spaces
  `self.mock_cabal.member_count = len(self.mock_members)`
- Line 30: Indentation over 4 spaces
  `return True, "Member added successfully"`
- Line 31: Indentation over 4 spaces
  ``
- Line 32: Indentation over 4 spaces
  `self.mock_cabal.add_member = mock_add_member`
- Line 33: Indentation over 4 spaces
  ``
- Line 34: Indentation over 4 spaces
  `# Mock the remove_member method`
- Line 35: Indentation over 4 spaces
  `def mock_remove_member(chad_id):`
- Line 36: Indentation over 4 spaces
  `if chad_id == self.mock_cabal.leader_id:`
- Line 37: Indentation over 4 spaces
  `return False, "Cannot remove leader"`
- Line 38: Indentation over 4 spaces
  `if chad_id not in self.mock_members:`
- Line 39: Indentation over 4 spaces
  `return False, "Member not in cabal"`
- Line 40: Indentation over 4 spaces
  `self.mock_members.remove(chad_id)`
- Line 41: Indentation over 4 spaces
  `self.mock_cabal.member_count = len(self.mock_members)`
- Line 42: Indentation over 4 spaces
  `return True, "Member removed successfully"`
- Line 43: Indentation over 4 spaces
  ``
- Line 44: Indentation over 4 spaces
  `self.mock_cabal.remove_member = mock_remove_member`
- Line 45: Indentation over 4 spaces
  ``
- Line 46: Indentation over 4 spaces
  `# Mock members list`
- Line 47: Indentation over 4 spaces
  `self.mock_members = []`
- Line 48: Indentation over 4 spaces
  ``
- Line 49: Indentation over 4 spaces
  `# Mock officers`
- Line 50: Indentation over 4 spaces
  `self.mock_officers = {}`
- Line 51: Indentation over 4 spaces
  ``
- Line 52: Indentation over 4 spaces
  `# Mock the appoint_officer method`
- Line 53: Indentation over 4 spaces
  `def mock_appoint_officer(chad_id, role):`
- Line 54: Indentation over 4 spaces
  `if chad_id == self.mock_cabal.leader_id:`
- Line 55: Indentation over 4 spaces
  `return False, "Cannot appoint leader as officer"`
- Line 56: Indentation over 4 spaces
  `if chad_id not in self.mock_members:`
- Line 57: Indentation over 4 spaces
  `return False, "Member not in cabal"`
- Line 58: Indentation over 4 spaces
  `if role not in ['clout', 'roast_level', 'cringe_resistance', 'drip_factor']:`
- Line 59: Indentation over 4 spaces
  `return False, "Invalid officer role"`
- Line 60: Indentation over 4 spaces
  ``
- Line 61: Indentation over 4 spaces
  `# Create mock officer`
- Line 62: Indentation over 4 spaces
  `mock_officer = MagicMock()`
- Line 63: Indentation over 4 spaces
  `mock_officer.cabal_id = self.cabal_id`
- Line 64: Indentation over 4 spaces
  `mock_officer.chad_id = chad_id`
- Line 65: Indentation over 4 spaces
  `mock_officer.role = role`
- Line 66: Indentation over 4 spaces
  ``
- Line 67: Indentation over 4 spaces
  `self.mock_officers[role] = mock_officer`
- Line 68: Indentation over 4 spaces
  `return True, f"Officer appointed for {role}"`
- Line 69: Indentation over 4 spaces
  ``
- Line 70: Indentation over 4 spaces
  `self.mock_cabal.appoint_officer = mock_appoint_officer`
- Line 71: Indentation over 4 spaces
  ``
- Line 72: Indentation over 4 spaces
  `# Mock the get_officer method`
- Line 73: Indentation over 4 spaces
  `def mock_get_officer(role):`
- Line 74: Indentation over 4 spaces
  `return self.mock_officers.get(role)`
- Line 75: Indentation over 4 spaces
  ``
- Line 76: Indentation over 4 spaces
  `self.mock_cabal.get_officer = mock_get_officer`
- Line 77: Indentation over 4 spaces
  ``
- Line 78: Indentation over 4 spaces
  `def test_cabal_creation(self):`
- Line 79: Indentation over 4 spaces
  `"""Test basic cabal properties"""`
- Line 80: Indentation over 4 spaces
  `# Check basic properties`
- Line 81: Indentation over 4 spaces
  `self.assertEqual(self.mock_cabal.name, "Test Cabal")`
- Line 82: Indentation over 4 spaces
  `self.assertEqual(self.mock_cabal.description, "A test cabal")`
- Line 83: Indentation over 4 spaces
  `self.assertEqual(self.mock_cabal.leader_id, self.test_chad_ids[0])`
- Line 84: Indentation over 4 spaces
  `self.assertEqual(self.mock_cabal.level, 1)`
- Line 85: Indentation over 4 spaces
  `self.assertEqual(self.mock_cabal.xp, 0)`
- Line 86: Indentation over 4 spaces
  `self.assertEqual(self.mock_cabal.invite_code, "ABC123")`
- Line 87: Indentation over 4 spaces
  `self.assertEqual(self.mock_cabal.member_count, 0)`
- Line 88: Indentation over 4 spaces
  ``
- Line 89: Indentation over 4 spaces
  `def test_add_member(self):`
- Line 90: Indentation over 4 spaces
  `"""Test adding members to a cabal"""`
- Line 91: Indentation over 4 spaces
  `# Add leader as member`
- Line 92: Indentation over 4 spaces
  `success, message = self.mock_cabal.add_member(self.test_chad_ids[0])`
- Line 93: Indentation over 4 spaces
  `self.assertTrue(success)`
- Line 94: Indentation over 4 spaces
  `self.assertEqual(self.mock_cabal.member_count, 1)`
- Line 95: Indentation over 4 spaces
  ``
- Line 96: Indentation over 4 spaces
  `# Add another member`
- Line 97: Indentation over 4 spaces
  `success, message = self.mock_cabal.add_member(self.test_chad_ids[1])`
- Line 98: Indentation over 4 spaces
  `self.assertTrue(success)`
- Line 99: Indentation over 4 spaces
  `self.assertEqual(self.mock_cabal.member_count, 2)`
- Line 100: Indentation over 4 spaces
  ``
- Line 101: Indentation over 4 spaces
  `# Try to add the same member again`
- Line 102: Indentation over 4 spaces
  `success, message = self.mock_cabal.add_member(self.test_chad_ids[1])`
- Line 103: Indentation over 4 spaces
  `self.assertFalse(success)`
- Line 104: Indentation over 4 spaces
  `self.assertEqual(self.mock_cabal.member_count, 2)`
- Line 105: Indentation over 4 spaces
  ``
- Line 106: Indentation over 4 spaces
  `def test_remove_member(self):`
- Line 107: Indentation over 4 spaces
  `"""Test removing members from a cabal"""`
- Line 108: Indentation over 4 spaces
  `# Add members`
- Line 109: Indentation over 4 spaces
  `self.mock_cabal.add_member(self.test_chad_ids[0])`
- Line 110: Indentation over 4 spaces
  `self.mock_cabal.add_member(self.test_chad_ids[1])`
- Line 111: Indentation over 4 spaces
  ``
- Line 112: Indentation over 4 spaces
  `# Try to remove the leader (should fail)`
- Line 113: Indentation over 4 spaces
  `success, message = self.mock_cabal.remove_member(self.test_chad_ids[0])`
- Line 114: Indentation over 4 spaces
  `self.assertFalse(success)`
- Line 115: Indentation over 4 spaces
  `self.assertEqual(self.mock_cabal.member_count, 2)`
- Line 116: Indentation over 4 spaces
  ``
- Line 117: Indentation over 4 spaces
  `# Remove a regular member`
- Line 118: Indentation over 4 spaces
  `success, message = self.mock_cabal.remove_member(self.test_chad_ids[1])`
- Line 119: Indentation over 4 spaces
  `self.assertTrue(success)`
- Line 120: Indentation over 4 spaces
  `self.assertEqual(self.mock_cabal.member_count, 1)`
- Line 121: Indentation over 4 spaces
  ``
- Line 122: Indentation over 4 spaces
  `def test_appoint_officer(self):`
- Line 123: Indentation over 4 spaces
  `"""Test appointing officers"""`
- Line 124: Indentation over 4 spaces
  `# Add members`
- Line 125: Indentation over 4 spaces
  `self.mock_cabal.add_member(self.test_chad_ids[0])`
- Line 126: Indentation over 4 spaces
  `self.mock_cabal.add_member(self.test_chad_ids[1])`
- Line 127: Indentation over 4 spaces
  ``
- Line 128: Indentation over 4 spaces
  `# Appoint an officer`
- Line 129: Indentation over 4 spaces
  `success, message = self.mock_cabal.appoint_officer(self.test_chad_ids[1], 'clout')`
- Line 130: Indentation over 4 spaces
  `self.assertTrue(success)`
- Line 131: Indentation over 4 spaces
  ``
- Line 132: Indentation over 4 spaces
  `# Verify officer was appointed`
- Line 133: Indentation over 4 spaces
  `officer = self.mock_cabal.get_officer('clout')`
- Line 134: Indentation over 4 spaces
  `self.assertIsNotNone(officer)`
- Line 135: Indentation over 4 spaces
  `self.assertEqual(officer.chad_id, self.test_chad_ids[1])`
- Line 136: Indentation over 4 spaces
  ``
- Line 137: Indentation over 4 spaces
  `# Try to appoint the leader (should fail)`
- Line 138: Indentation over 4 spaces
  `success, message = self.mock_cabal.appoint_officer(self.test_chad_ids[0], 'roast_level')`
- Line 139: Indentation over 4 spaces
  `self.assertFalse(success)`
- Line 140: Indentation over 4 spaces
  ``
- Line 141: Indentation over 4 spaces
  `# Try to appoint invalid role`
- Line 142: Indentation over 4 spaces
  `success, message = self.mock_cabal.appoint_officer(self.test_chad_ids[1], 'invalid_role')`
- Line 143: Indentation over 4 spaces
  `self.assertFalse(success)`

### tests\test_cabal_model.py (365 issues)

#### Code Smells
- Line 45: Debug print statement
  `print(f"Error creating table {table.name}: {e}")`
- Line 75: Explicit commit - check transaction management
  `db.session.commit()`
- Line 91: Explicit commit - check transaction management
  `db.session.commit()`
- Line 114: Explicit commit - check transaction management
  `db.session.commit()`
- Line 139: Explicit commit - check transaction management
  `db.session.commit()`
- Line 163: Explicit commit - check transaction management
  `db.session.commit()`
- Line 194: Explicit commit - check transaction management
  `db.session.commit()`
- Line 218: Explicit commit - check transaction management
  `db.session.commit()`
- Line 260: Explicit commit - check transaction management
  `db.session.commit()`
- Line 293: Explicit commit - check transaction management
  `db.session.commit()`
- Line 327: Explicit commit - check transaction management
  `db.session.commit()`
- Line 37: Bare except clause
  `except:`
- Line 44: Catching Exception - too broad
  `except Exception as e:`
- Line 263: Datetime usage - check for timezone awareness
  `battle_time = datetime.utcnow() + timedelta(days=1)`
- Line 339: Datetime usage - check for timezone awareness
  `battle_time = datetime.utcnow() + timedelta(days=1)`

#### Best Practice Violations
- Line 15: Function without docstring
  `def setUp(self):`
- Line 77: Function without docstring
  `def tearDown(self):`
- Line 83: Function without docstring
  `def test_cabal_creation(self):`
- Line 106: Function without docstring
  `def test_add_member(self):`
- Line 131: Function without docstring
  `def test_remove_member(self):`
- Line 155: Function without docstring
  `def test_appoint_officer(self):`
- Line 186: Function without docstring
  `def test_change_leader(self):`
- Line 210: Function without docstring
  `def test_voting(self):`
- Line 247: Function without docstring
  `def test_battle_scheduling(self):`
- Line 285: Function without docstring
  `def test_calculate_total_power(self):`
- Line 319: Function without docstring
  `def test_disband(self):`
- Line 18: Self assignment in method/constructor
  `self.app_context = self.app.app_context()`
- Line 15: Indentation over 4 spaces
  `def setUp(self):`
- Line 16: Indentation over 4 spaces
  `"""Set up test environment before each test"""`
- Line 17: Indentation over 4 spaces
  `self.app = create_app('testing')`
- Line 18: Indentation over 4 spaces
  `self.app_context = self.app.app_context()`
- Line 19: Indentation over 4 spaces
  `self.app_context.push()`
- Line 20: Indentation over 4 spaces
  ``
- Line 21: Indentation over 4 spaces
  `# Instead of creating all tables, we'll create only the ones we need`
- Line 22: Indentation over 4 spaces
  `# This avoids foreign key issues with tables that have complex dependencies`
- Line 23: Indentation over 4 spaces
  `tables_to_create = [`
- Line 24: Indentation over 4 spaces
  `User.__table__,`
- Line 25: Indentation over 4 spaces
  `Chad.__table__,`
- Line 26: Indentation over 4 spaces
  `Cabal.__table__,`
- Line 27: Indentation over 4 spaces
  `CabalMember.__table__,`
- Line 28: Indentation over 4 spaces
  `CabalOfficerRole.__table__,`
- Line 29: Indentation over 4 spaces
  `CabalVote.__table__,`
- Line 30: Indentation over 4 spaces
  `CabalBattle.__table__`
- Line 31: Indentation over 4 spaces
  `]`
- Line 32: Indentation over 4 spaces
  ``
- Line 33: Indentation over 4 spaces
  `# Drop tables if they exist`
- Line 34: Indentation over 4 spaces
  `for table in reversed(tables_to_create):`
- Line 35: Indentation over 4 spaces
  `try:`
- Line 36: Indentation over 4 spaces
  `table.drop(db.engine, checkfirst=True)`
- Line 37: Indentation over 4 spaces
  `except:`
- Line 38: Indentation over 4 spaces
  `pass`
- Line 39: Indentation over 4 spaces
  ``
- Line 40: Indentation over 4 spaces
  `# Create only the tables we need`
- Line 41: Indentation over 4 spaces
  `for table in tables_to_create:`
- Line 42: Indentation over 4 spaces
  `try:`
- Line 43: Indentation over 4 spaces
  `table.create(db.engine, checkfirst=True)`
- Line 44: Indentation over 4 spaces
  `except Exception as e:`
- Line 45: Indentation over 4 spaces
  `print(f"Error creating table {table.name}: {e}")`
- Line 46: Indentation over 4 spaces
  ``
- Line 47: Indentation over 4 spaces
  `# Create test users and chads`
- Line 48: Indentation over 4 spaces
  `self.test_users = []`
- Line 49: Indentation over 4 spaces
  `self.test_chads = []`
- Line 50: Indentation over 4 spaces
  ``
- Line 51: Indentation over 4 spaces
  `for i in range(5):`
- Line 52: Indentation over 4 spaces
  `user = User(`
- Line 53: Indentation over 4 spaces
  `id=str(uuid.uuid4()),`
- Line 54: Indentation over 4 spaces
  `twitter_handle=f'test_user_{i}',`
- Line 55: Indentation over 4 spaces
  `twitter_id=f'{1000+i}',`
- Line 56: Indentation over 4 spaces
  `email=f'test{i}@example.com'`
- Line 57: Indentation over 4 spaces
  `)`
- Line 58: Indentation over 4 spaces
  `db.session.add(user)`
- Line 59: Indentation over 4 spaces
  `db.session.flush()  # Flush to get the IDs`
- Line 60: Indentation over 4 spaces
  ``
- Line 61: Indentation over 4 spaces
  `chad = Chad(`
- Line 62: Indentation over 4 spaces
  `id=str(uuid.uuid4()),`
- Line 63: Indentation over 4 spaces
  `name=f'Test Chad {i}',`
- Line 64: Indentation over 4 spaces
  `clout=10 + i,`
- Line 65: Indentation over 4 spaces
  `roast_level=20 + i,`
- Line 66: Indentation over 4 spaces
  `cringe_resistance=15 + i,`
- Line 67: Indentation over 4 spaces
  `drip_factor=25 + i,`
- Line 68: Indentation over 4 spaces
  `user_id=user.id`
- Line 69: Indentation over 4 spaces
  `)`
- Line 70: Indentation over 4 spaces
  `db.session.add(chad)`
- Line 71: Indentation over 4 spaces
  ``
- Line 72: Indentation over 4 spaces
  `self.test_users.append(user)`
- Line 73: Indentation over 4 spaces
  `self.test_chads.append(chad)`
- Line 74: Indentation over 4 spaces
  ``
- Line 75: Indentation over 4 spaces
  `db.session.commit()`
- Line 76: Indentation over 4 spaces
  ``
- Line 77: Indentation over 4 spaces
  `def tearDown(self):`
- Line 78: Indentation over 4 spaces
  `"""Clean up after each test"""`
- Line 79: Indentation over 4 spaces
  `db.session.remove()`
- Line 80: Indentation over 4 spaces
  `# Don't drop all tables, just clear the session`
- Line 81: Indentation over 4 spaces
  `self.app_context.pop()`
- Line 82: Indentation over 4 spaces
  ``
- Line 83: Indentation over 4 spaces
  `def test_cabal_creation(self):`
- Line 84: Indentation over 4 spaces
  `"""Test basic cabal creation"""`
- Line 85: Indentation over 4 spaces
  `cabal = Cabal(`
- Line 86: Indentation over 4 spaces
  `name="Test Cabal",`
- Line 87: Indentation over 4 spaces
  `description="A test cabal",`
- Line 88: Indentation over 4 spaces
  `leader_id=self.test_chads[0].id`
- Line 89: Indentation over 4 spaces
  `)`
- Line 90: Indentation over 4 spaces
  `db.session.add(cabal)`
- Line 91: Indentation over 4 spaces
  `db.session.commit()`
- Line 92: Indentation over 4 spaces
  ``
- Line 93: Indentation over 4 spaces
  `# Check basic properties`
- Line 94: Indentation over 4 spaces
  `self.assertEqual(cabal.name, "Test Cabal")`
- Line 95: Indentation over 4 spaces
  `self.assertEqual(cabal.description, "A test cabal")`
- Line 96: Indentation over 4 spaces
  `self.assertEqual(cabal.leader_id, self.test_chads[0].id)`
- Line 97: Indentation over 4 spaces
  `self.assertEqual(cabal.level, 1)`
- Line 98: Indentation over 4 spaces
  `self.assertEqual(cabal.xp, 0)`
- Line 99: Indentation over 4 spaces
  `self.assertTrue(cabal.invite_code)  # Should auto-generate`
- Line 100: Indentation over 4 spaces
  `self.assertEqual(cabal.member_count, 0)`
- Line 101: Indentation over 4 spaces
  ``
- Line 102: Indentation over 4 spaces
  `# Test invite code generation`
- Line 103: Indentation over 4 spaces
  `self.assertIsNotNone(cabal.invite_code)`
- Line 104: Indentation over 4 spaces
  `self.assertEqual(len(cabal.invite_code), 6)`
- Line 105: Indentation over 4 spaces
  ``
- Line 106: Indentation over 4 spaces
  `def test_add_member(self):`
- Line 107: Indentation over 4 spaces
  `"""Test adding members to a cabal"""`
- Line 108: Indentation over 4 spaces
  `cabal = Cabal(`
- Line 109: Indentation over 4 spaces
  `name="Member Test Cabal",`
- Line 110: Indentation over 4 spaces
  `description="Testing member functions",`
- Line 111: Indentation over 4 spaces
  `leader_id=self.test_chads[0].id`
- Line 112: Indentation over 4 spaces
  `)`
- Line 113: Indentation over 4 spaces
  `db.session.add(cabal)`
- Line 114: Indentation over 4 spaces
  `db.session.commit()`
- Line 115: Indentation over 4 spaces
  ``
- Line 116: Indentation over 4 spaces
  `# Add leader as member`
- Line 117: Indentation over 4 spaces
  `success, message = cabal.add_member(self.test_chads[0].id)`
- Line 118: Indentation over 4 spaces
  `self.assertTrue(success)`
- Line 119: Indentation over 4 spaces
  `self.assertEqual(cabal.member_count, 1)`
- Line 120: Indentation over 4 spaces
  ``
- Line 121: Indentation over 4 spaces
  `# Add another member`
- Line 122: Indentation over 4 spaces
  `success, message = cabal.add_member(self.test_chads[1].id)`
- Line 123: Indentation over 4 spaces
  `self.assertTrue(success)`
- Line 124: Indentation over 4 spaces
  `self.assertEqual(cabal.member_count, 2)`
- Line 125: Indentation over 4 spaces
  ``
- Line 126: Indentation over 4 spaces
  `# Try to add the same member again`
- Line 127: Indentation over 4 spaces
  `success, message = cabal.add_member(self.test_chads[1].id)`
- Line 128: Indentation over 4 spaces
  `self.assertFalse(success)`
- Line 129: Indentation over 4 spaces
  `self.assertEqual(cabal.member_count, 2)`
- Line 130: Indentation over 4 spaces
  ``
- Line 131: Indentation over 4 spaces
  `def test_remove_member(self):`
- Line 132: Indentation over 4 spaces
  `"""Test removing members from a cabal"""`
- Line 133: Indentation over 4 spaces
  `cabal = Cabal(`
- Line 134: Indentation over 4 spaces
  `name="Remove Test Cabal",`
- Line 135: Indentation over 4 spaces
  `description="Testing removal functions",`
- Line 136: Indentation over 4 spaces
  `leader_id=self.test_chads[0].id`
- Line 137: Indentation over 4 spaces
  `)`
- Line 138: Indentation over 4 spaces
  `db.session.add(cabal)`
- Line 139: Indentation over 4 spaces
  `db.session.commit()`
- Line 140: Indentation over 4 spaces
  ``
- Line 141: Indentation over 4 spaces
  `# Add members`
- Line 142: Indentation over 4 spaces
  `cabal.add_member(self.test_chads[0].id)`
- Line 143: Indentation over 4 spaces
  `cabal.add_member(self.test_chads[1].id)`
- Line 144: Indentation over 4 spaces
  ``
- Line 145: Indentation over 4 spaces
  `# Try to remove the leader (should fail)`
- Line 146: Indentation over 4 spaces
  `success, message = cabal.remove_member(self.test_chads[0].id)`
- Line 147: Indentation over 4 spaces
  `self.assertFalse(success)`
- Line 148: Indentation over 4 spaces
  `self.assertEqual(cabal.member_count, 2)`
- Line 149: Indentation over 4 spaces
  ``
- Line 150: Indentation over 4 spaces
  `# Remove a regular member`
- Line 151: Indentation over 4 spaces
  `success, message = cabal.remove_member(self.test_chads[1].id)`
- Line 152: Indentation over 4 spaces
  `self.assertTrue(success)`
- Line 153: Indentation over 4 spaces
  `self.assertEqual(cabal.member_count, 1)`
- Line 154: Indentation over 4 spaces
  ``
- Line 155: Indentation over 4 spaces
  `def test_appoint_officer(self):`
- Line 156: Indentation over 4 spaces
  `"""Test appointing officers"""`
- Line 157: Indentation over 4 spaces
  `cabal = Cabal(`
- Line 158: Indentation over 4 spaces
  `name="Officer Test Cabal",`
- Line 159: Indentation over 4 spaces
  `description="Testing officer functions",`
- Line 160: Indentation over 4 spaces
  `leader_id=self.test_chads[0].id`
- Line 161: Indentation over 4 spaces
  `)`
- Line 162: Indentation over 4 spaces
  `db.session.add(cabal)`
- Line 163: Indentation over 4 spaces
  `db.session.commit()`
- Line 164: Indentation over 4 spaces
  ``
- Line 165: Indentation over 4 spaces
  `# Add members`
- Line 166: Indentation over 4 spaces
  `cabal.add_member(self.test_chads[0].id)`
- Line 167: Indentation over 4 spaces
  `cabal.add_member(self.test_chads[1].id)`
- Line 168: Indentation over 4 spaces
  ``
- Line 169: Indentation over 4 spaces
  `# Appoint an officer`
- Line 170: Indentation over 4 spaces
  `success, message = cabal.appoint_officer(self.test_chads[1].id, 'clout')`
- Line 171: Indentation over 4 spaces
  `self.assertTrue(success)`
- Line 172: Indentation over 4 spaces
  ``
- Line 173: Indentation over 4 spaces
  `# Verify officer was appointed`
- Line 174: Indentation over 4 spaces
  `officer = cabal.get_officer('clout')`
- Line 175: Indentation over 4 spaces
  `self.assertIsNotNone(officer)`
- Line 176: Indentation over 4 spaces
  `self.assertEqual(officer.chad_id, self.test_chads[1].id)`
- Line 177: Indentation over 4 spaces
  ``
- Line 178: Indentation over 4 spaces
  `# Try to appoint the leader (should fail)`
- Line 179: Indentation over 4 spaces
  `success, message = cabal.appoint_officer(self.test_chads[0].id, 'roast_level')`
- Line 180: Indentation over 4 spaces
  `self.assertFalse(success)`
- Line 181: Indentation over 4 spaces
  ``
- Line 182: Indentation over 4 spaces
  `# Try to appoint invalid role`
- Line 183: Indentation over 4 spaces
  `success, message = cabal.appoint_officer(self.test_chads[1].id, 'invalid_role')`
- Line 184: Indentation over 4 spaces
  `self.assertFalse(success)`
- Line 185: Indentation over 4 spaces
  ``
- Line 186: Indentation over 4 spaces
  `def test_change_leader(self):`
- Line 187: Indentation over 4 spaces
  `"""Test changing cabal leadership"""`
- Line 188: Indentation over 4 spaces
  `cabal = Cabal(`
- Line 189: Indentation over 4 spaces
  `name="Leadership Test Cabal",`
- Line 190: Indentation over 4 spaces
  `description="Testing leadership changes",`
- Line 191: Indentation over 4 spaces
  `leader_id=self.test_chads[0].id`
- Line 192: Indentation over 4 spaces
  `)`
- Line 193: Indentation over 4 spaces
  `db.session.add(cabal)`
- Line 194: Indentation over 4 spaces
  `db.session.commit()`
- Line 195: Indentation over 4 spaces
  ``
- Line 196: Indentation over 4 spaces
  `# Add members`
- Line 197: Indentation over 4 spaces
  `cabal.add_member(self.test_chads[0].id)`
- Line 198: Indentation over 4 spaces
  `cabal.add_member(self.test_chads[1].id)`
- Line 199: Indentation over 4 spaces
  ``
- Line 200: Indentation over 4 spaces
  `# Change leader`
- Line 201: Indentation over 4 spaces
  `success, message = cabal.change_leader(self.test_chads[1].id)`
- Line 202: Indentation over 4 spaces
  `self.assertTrue(success)`
- Line 203: Indentation over 4 spaces
  `self.assertEqual(cabal.leader_id, self.test_chads[1].id)`
- Line 204: Indentation over 4 spaces
  ``
- Line 205: Indentation over 4 spaces
  `# Try to change to non-member`
- Line 206: Indentation over 4 spaces
  `success, message = cabal.change_leader(self.test_chads[2].id)`
- Line 207: Indentation over 4 spaces
  `self.assertFalse(success)`
- Line 208: Indentation over 4 spaces
  `self.assertEqual(cabal.leader_id, self.test_chads[1].id)`
- Line 209: Indentation over 4 spaces
  ``
- Line 210: Indentation over 4 spaces
  `def test_voting(self):`
- Line 211: Indentation over 4 spaces
  `"""Test voting mechanics"""`
- Line 212: Indentation over 4 spaces
  `cabal = Cabal(`
- Line 213: Indentation over 4 spaces
  `name="Voting Test Cabal",`
- Line 214: Indentation over 4 spaces
  `description="Testing voting mechanics",`
- Line 215: Indentation over 4 spaces
  `leader_id=self.test_chads[0].id`
- Line 216: Indentation over 4 spaces
  `)`
- Line 217: Indentation over 4 spaces
  `db.session.add(cabal)`
- Line 218: Indentation over 4 spaces
  `db.session.commit()`
- Line 219: Indentation over 4 spaces
  ``
- Line 220: Indentation over 4 spaces
  `# Add members - need at least 4 for meaningful vote test`
- Line 221: Indentation over 4 spaces
  `for i in range(4):`
- Line 222: Indentation over 4 spaces
  `cabal.add_member(self.test_chads[i].id)`
- Line 223: Indentation over 4 spaces
  ``
- Line 224: Indentation over 4 spaces
  `# Add officers`
- Line 225: Indentation over 4 spaces
  `cabal.appoint_officer(self.test_chads[1].id, 'clout')`
- Line 226: Indentation over 4 spaces
  `cabal.appoint_officer(self.test_chads[2].id, 'roast_level')`
- Line 227: Indentation over 4 spaces
  ``
- Line 228: Indentation over 4 spaces
  `# Cast votes to remove leader`
- Line 229: Indentation over 4 spaces
  `success, message = cabal.vote_to_remove_leader(self.test_chads[1].id)`
- Line 230: Indentation over 4 spaces
  `self.assertTrue(success)`
- Line 231: Indentation over 4 spaces
  ``
- Line 232: Indentation over 4 spaces
  `success, message = cabal.vote_to_remove_leader(self.test_chads[2].id)`
- Line 233: Indentation over 4 spaces
  `self.assertTrue(success)`
- Line 234: Indentation over 4 spaces
  ``
- Line 235: Indentation over 4 spaces
  `# Try to vote twice (should fail)`
- Line 236: Indentation over 4 spaces
  `success, message = cabal.vote_to_remove_leader(self.test_chads[1].id)`
- Line 237: Indentation over 4 spaces
  `self.assertFalse(success)`
- Line 238: Indentation over 4 spaces
  ``
- Line 239: Indentation over 4 spaces
  `# Check vote count`
- Line 240: Indentation over 4 spaces
  `vote_count = CabalVote.query.filter_by(`
- Line 241: Indentation over 4 spaces
  `cabal_id=cabal.id,`
- Line 242: Indentation over 4 spaces
  `vote_type='remove_leader',`
- Line 243: Indentation over 4 spaces
  `target_id=cabal.leader_id`
- Line 244: Indentation over 4 spaces
  `).count()`
- Line 245: Indentation over 4 spaces
  `self.assertEqual(vote_count, 2)`
- Line 246: Indentation over 4 spaces
  ``
- Line 247: Indentation over 4 spaces
  `def test_battle_scheduling(self):`
- Line 248: Indentation over 4 spaces
  `"""Test battle scheduling mechanics"""`
- Line 249: Indentation over 4 spaces
  `cabal1 = Cabal(`
- Line 250: Indentation over 4 spaces
  `name="Battle Test Cabal 1",`
- Line 251: Indentation over 4 spaces
  `description="Testing battle scheduling",`
- Line 252: Indentation over 4 spaces
  `leader_id=self.test_chads[0].id`
- Line 253: Indentation over 4 spaces
  `)`
- Line 254: Indentation over 4 spaces
  `cabal2 = Cabal(`
- Line 255: Indentation over 4 spaces
  `name="Battle Test Cabal 2",`
- Line 256: Indentation over 4 spaces
  `description="Testing battle scheduling",`
- Line 257: Indentation over 4 spaces
  `leader_id=self.test_chads[1].id`
- Line 258: Indentation over 4 spaces
  `)`
- Line 259: Indentation over 4 spaces
  `db.session.add_all([cabal1, cabal2])`
- Line 260: Indentation over 4 spaces
  `db.session.commit()`
- Line 261: Indentation over 4 spaces
  ``
- Line 262: Indentation over 4 spaces
  `# Schedule a battle`
- Line 263: Indentation over 4 spaces
  `battle_time = datetime.utcnow() + timedelta(days=1)`
- Line 264: Indentation over 4 spaces
  `success, message = cabal1.schedule_battle(cabal2.id, battle_time)`
- Line 265: Indentation over 4 spaces
  `self.assertTrue(success)`
- Line 266: Indentation over 4 spaces
  ``
- Line 267: Indentation over 4 spaces
  `# Check if battle was created`
- Line 268: Indentation over 4 spaces
  `battle = CabalBattle.query.filter_by(cabal_id=cabal1.id).first()`
- Line 269: Indentation over 4 spaces
  `self.assertIsNotNone(battle)`
- Line 270: Indentation over 4 spaces
  `self.assertEqual(battle.opponent_cabal_id, cabal2.id)`
- Line 271: Indentation over 4 spaces
  `self.assertEqual(battle.scheduled_at, battle_time)`
- Line 272: Indentation over 4 spaces
  ``
- Line 273: Indentation over 4 spaces
  `# Test battle limits (3 per week)`
- Line 274: Indentation over 4 spaces
  `for i in range(2):`
- Line 275: Indentation over 4 spaces
  `cabal1.schedule_battle(cabal2.id, battle_time + timedelta(hours=i+1))`
- Line 276: Indentation over 4 spaces
  ``
- Line 277: Indentation over 4 spaces
  `# This should hit the limit`
- Line 278: Indentation over 4 spaces
  `success, message = cabal1.schedule_battle(cabal2.id, battle_time + timedelta(hours=4))`
- Line 279: Indentation over 4 spaces
  `self.assertFalse(success)`
- Line 280: Indentation over 4 spaces
  ``
- Line 281: Indentation over 4 spaces
  `# Check battle count`
- Line 282: Indentation over 4 spaces
  `battle_count = CabalBattle.query.filter_by(cabal_id=cabal1.id).count()`
- Line 283: Indentation over 4 spaces
  `self.assertEqual(battle_count, 3)`
- Line 284: Indentation over 4 spaces
  ``
- Line 285: Indentation over 4 spaces
  `def test_calculate_total_power(self):`
- Line 286: Indentation over 4 spaces
  `"""Test cabal power calculation with officers"""`
- Line 287: Indentation over 4 spaces
  `cabal = Cabal(`
- Line 288: Indentation over 4 spaces
  `name="Power Test Cabal",`
- Line 289: Indentation over 4 spaces
  `description="Testing power calculation",`
- Line 290: Indentation over 4 spaces
  `leader_id=self.test_chads[0].id`
- Line 291: Indentation over 4 spaces
  `)`
- Line 292: Indentation over 4 spaces
  `db.session.add(cabal)`
- Line 293: Indentation over 4 spaces
  `db.session.commit()`
- Line 294: Indentation over 4 spaces
  ``
- Line 295: Indentation over 4 spaces
  `# Add members with known stats`
- Line 296: Indentation over 4 spaces
  `for i in range(3):`
- Line 297: Indentation over 4 spaces
  `cabal.add_member(self.test_chads[i].id)`
- Line 298: Indentation over 4 spaces
  ``
- Line 299: Indentation over 4 spaces
  `# Appoint officers`
- Line 300: Indentation over 4 spaces
  `cabal.appoint_officer(self.test_chads[1].id, 'clout')`
- Line 301: Indentation over 4 spaces
  `cabal.appoint_officer(self.test_chads[2].id, 'roast_level')`
- Line 302: Indentation over 4 spaces
  ``
- Line 303: Indentation over 4 spaces
  `# Calculate power`
- Line 304: Indentation over 4 spaces
  `power = cabal.calculate_total_power()`
- Line 305: Indentation over 4 spaces
  ``
- Line 306: Indentation over 4 spaces
  `# Verify power calculation`
- Line 307: Indentation over 4 spaces
  `self.assertGreater(power, 0)`
- Line 308: Indentation over 4 spaces
  `# Full formula verification would be more complex, but we can check it's reasonable`
- Line 309: Indentation over 4 spaces
  `self.assertTrue(isinstance(power, float))`
- Line 310: Indentation over 4 spaces
  ``
- Line 311: Indentation over 4 spaces
  `# Recalculate with a debuff`
- Line 312: Indentation over 4 spaces
  `cabal.apply_debuff('test_debuff')`
- Line 313: Indentation over 4 spaces
  `debuffed_power = cabal.calculate_total_power()`
- Line 314: Indentation over 4 spaces
  ``
- Line 315: Indentation over 4 spaces
  `# Debuffed power should be 90% of normal power`
- Line 316: Indentation over 4 spaces
  `self.assertLess(debuffed_power, power)`
- Line 317: Indentation over 4 spaces
  `self.assertAlmostEqual(debuffed_power / power, 0.9, delta=0.01)`
- Line 318: Indentation over 4 spaces
  ``
- Line 319: Indentation over 4 spaces
  `def test_disband(self):`
- Line 320: Indentation over 4 spaces
  `"""Test disbanding a cabal"""`
- Line 321: Indentation over 4 spaces
  `cabal = Cabal(`
- Line 322: Indentation over 4 spaces
  `name="Disband Test Cabal",`
- Line 323: Indentation over 4 spaces
  `description="Testing disband function",`
- Line 324: Indentation over 4 spaces
  `leader_id=self.test_chads[0].id`
- Line 325: Indentation over 4 spaces
  `)`
- Line 326: Indentation over 4 spaces
  `db.session.add(cabal)`
- Line 327: Indentation over 4 spaces
  `db.session.commit()`
- Line 328: Indentation over 4 spaces
  ``
- Line 329: Indentation over 4 spaces
  `cabal_id = cabal.id`
- Line 330: Indentation over 4 spaces
  ``
- Line 331: Indentation over 4 spaces
  `# Add members`
- Line 332: Indentation over 4 spaces
  `for i in range(3):`
- Line 333: Indentation over 4 spaces
  `cabal.add_member(self.test_chads[i].id)`
- Line 334: Indentation over 4 spaces
  ``
- Line 335: Indentation over 4 spaces
  `# Appoint officer`
- Line 336: Indentation over 4 spaces
  `cabal.appoint_officer(self.test_chads[1].id, 'clout')`
- Line 337: Indentation over 4 spaces
  ``
- Line 338: Indentation over 4 spaces
  `# Schedule battle`
- Line 339: Indentation over 4 spaces
  `battle_time = datetime.utcnow() + timedelta(days=1)`
- Line 340: Indentation over 4 spaces
  `cabal.schedule_battle(None, battle_time)`
- Line 341: Indentation over 4 spaces
  ``
- Line 342: Indentation over 4 spaces
  `# Disband the cabal`
- Line 343: Indentation over 4 spaces
  `success, message = cabal.disband()`
- Line 344: Indentation over 4 spaces
  `self.assertTrue(success)`
- Line 345: Indentation over 4 spaces
  ``
- Line 346: Indentation over 4 spaces
  `# Verify everything was deleted`
- Line 347: Indentation over 4 spaces
  `self.assertIsNone(Cabal.query.get(cabal_id))`
- Line 348: Indentation over 4 spaces
  `self.assertEqual(CabalMember.query.filter_by(cabal_id=cabal_id).count(), 0)`
- Line 349: Indentation over 4 spaces
  `self.assertEqual(CabalOfficerRole.query.filter_by(cabal_id=cabal_id).count(), 0)`
- Line 350: Indentation over 4 spaces
  `self.assertEqual(CabalBattle.query.filter_by(cabal_id=cabal_id).count(), 0)`
- Line 351: Indentation over 4 spaces
  `self.assertEqual(CabalVote.query.filter_by(cabal_id=cabal_id).count(), 0)`
- Line 354: Indentation over 4 spaces
  `unittest.main()`

### tests\test_cabal_routes.py (301 issues)

#### Code Smells
- Line 67: Explicit commit - check transaction management
  `db.session.commit()`
- Line 76: Explicit commit - check transaction management
  `db.session.commit()`
- Line 102: Explicit commit - check transaction management
  `db.session.commit()`
- Line 161: Explicit commit - check transaction management
  `db.session.commit()`
- Line 191: Explicit commit - check transaction management
  `db.session.commit()`
- Line 247: Explicit commit - check transaction management
  `db.session.commit()`
- Line 266: Explicit commit - check transaction management
  `db.session.commit()`
- Line 163: Datetime usage - check for timezone awareness
  `tomorrow = datetime.utcnow() + timedelta(days=1)`
- Line 187: Datetime usage - check for timezone awareness
  `scheduled_at=datetime.utcnow() + timedelta(days=1),`
- Line 232: Datetime usage - check for timezone awareness
  `scheduled_at=datetime.utcnow() + timedelta(days=i+1),`
- Line 241: Datetime usage - check for timezone awareness
  `scheduled_at=datetime.utcnow() - timedelta(days=1),`

#### Best Practice Violations
- Line 12: Function without docstring
  `def setUp(self):`
- Line 85: Function without docstring
  `def tearDown(self):`
- Line 91: Function without docstring
  `def test_index_route(self):`
- Line 97: Function without docstring
  `def test_create_cabal(self):`
- Line 119: Function without docstring
  `def test_appoint_officer(self):`
- Line 137: Function without docstring
  `def test_remove_officer(self):`
- Line 152: Function without docstring
  `def test_schedule_battle(self):`
- Line 181: Function without docstring
  `def test_opt_into_battle(self):`
- Line 203: Function without docstring
  `def test_vote_remove_leader(self):`
- Line 225: Function without docstring
  `def test_all_battles(self):`
- Line 255: Function without docstring
  `def test_leaderboard(self):`
- Line 274: Function without docstring
  `def test_disband_cabal(self):`
- Line 15: Self assignment in method/constructor
  `self.app_context = self.app.app_context()`
- Line 17: Self assignment in method/constructor
  `self.client = self.app.test_client()`
- Line 37: Self assignment in method/constructor
  `self.user.chad_id = self.chad.id`
- Line 12: Indentation over 4 spaces
  `def setUp(self):`
- Line 13: Indentation over 4 spaces
  `"""Set up test environment before each test"""`
- Line 14: Indentation over 4 spaces
  `self.app = create_app('testing')`
- Line 15: Indentation over 4 spaces
  `self.app_context = self.app.app_context()`
- Line 16: Indentation over 4 spaces
  `self.app_context.push()`
- Line 17: Indentation over 4 spaces
  `self.client = self.app.test_client()`
- Line 18: Indentation over 4 spaces
  `db.create_all()`
- Line 19: Indentation over 4 spaces
  ``
- Line 20: Indentation over 4 spaces
  `# Create test user and chad`
- Line 21: Indentation over 4 spaces
  `self.user = User(`
- Line 22: Indentation over 4 spaces
  `id=str(uuid.uuid4()),`
- Line 23: Indentation over 4 spaces
  `twitter_handle='test_user',`
- Line 24: Indentation over 4 spaces
  `twitter_id='12345',`
- Line 25: Indentation over 4 spaces
  `email='test@example.com'`
- Line 26: Indentation over 4 spaces
  `)`
- Line 27: Indentation over 4 spaces
  ``
- Line 28: Indentation over 4 spaces
  `self.chad = Chad(`
- Line 29: Indentation over 4 spaces
  `id=str(uuid.uuid4()),`
- Line 30: Indentation over 4 spaces
  `name='Test Chad',`
- Line 31: Indentation over 4 spaces
  `clout=10,`
- Line 32: Indentation over 4 spaces
  `roast_level=20,`
- Line 33: Indentation over 4 spaces
  `cringe_resistance=15,`
- Line 34: Indentation over 4 spaces
  `drip_factor=25`
- Line 35: Indentation over 4 spaces
  `)`
- Line 36: Indentation over 4 spaces
  ``
- Line 37: Indentation over 4 spaces
  `self.user.chad_id = self.chad.id`
- Line 38: Indentation over 4 spaces
  `db.session.add_all([self.user, self.chad])`
- Line 39: Indentation over 4 spaces
  ``
- Line 40: Indentation over 4 spaces
  `# Create additional users for testing`
- Line 41: Indentation over 4 spaces
  `self.other_users = []`
- Line 42: Indentation over 4 spaces
  `self.other_chads = []`
- Line 43: Indentation over 4 spaces
  ``
- Line 44: Indentation over 4 spaces
  `for i in range(5):`
- Line 45: Indentation over 4 spaces
  `user = User(`
- Line 46: Indentation over 4 spaces
  `id=str(uuid.uuid4()),`
- Line 47: Indentation over 4 spaces
  `twitter_handle=f'test_user_{i}',`
- Line 48: Indentation over 4 spaces
  `twitter_id=f'{1000+i}',`
- Line 49: Indentation over 4 spaces
  `email=f'test{i}@example.com'`
- Line 50: Indentation over 4 spaces
  `)`
- Line 51: Indentation over 4 spaces
  ``
- Line 52: Indentation over 4 spaces
  `chad = Chad(`
- Line 53: Indentation over 4 spaces
  `id=str(uuid.uuid4()),`
- Line 54: Indentation over 4 spaces
  `name=f'Test Chad {i}',`
- Line 55: Indentation over 4 spaces
  `clout=10 + i,`
- Line 56: Indentation over 4 spaces
  `roast_level=20 + i,`
- Line 57: Indentation over 4 spaces
  `cringe_resistance=15 + i,`
- Line 58: Indentation over 4 spaces
  `drip_factor=25 + i`
- Line 59: Indentation over 4 spaces
  `)`
- Line 60: Indentation over 4 spaces
  ``
- Line 61: Indentation over 4 spaces
  `user.chad_id = chad.id`
- Line 62: Indentation over 4 spaces
  `db.session.add_all([user, chad])`
- Line 63: Indentation over 4 spaces
  ``
- Line 64: Indentation over 4 spaces
  `self.other_users.append(user)`
- Line 65: Indentation over 4 spaces
  `self.other_chads.append(chad)`
- Line 66: Indentation over 4 spaces
  ``
- Line 67: Indentation over 4 spaces
  `db.session.commit()`
- Line 68: Indentation over 4 spaces
  ``
- Line 69: Indentation over 4 spaces
  `# Create a test cabal`
- Line 70: Indentation over 4 spaces
  `self.cabal = Cabal(`
- Line 71: Indentation over 4 spaces
  `name="Test Cabal",`
- Line 72: Indentation over 4 spaces
  `description="A test cabal",`
- Line 73: Indentation over 4 spaces
  `leader_id=self.chad.id`
- Line 74: Indentation over 4 spaces
  `)`
- Line 75: Indentation over 4 spaces
  `db.session.add(self.cabal)`
- Line 76: Indentation over 4 spaces
  `db.session.commit()`
- Line 77: Indentation over 4 spaces
  ``
- Line 78: Indentation over 4 spaces
  `# Add the leader as a member`
- Line 79: Indentation over 4 spaces
  `self.cabal.add_member(self.chad.id)`
- Line 80: Indentation over 4 spaces
  ``
- Line 81: Indentation over 4 spaces
  `# Helper to perform login`
- Line 82: Indentation over 4 spaces
  `with self.client.session_transaction() as session:`
- Line 83: Indentation over 4 spaces
  `session['_user_id'] = str(self.user.id)`
- Line 84: Indentation over 4 spaces
  ``
- Line 85: Indentation over 4 spaces
  `def tearDown(self):`
- Line 86: Indentation over 4 spaces
  `"""Clean up after each test"""`
- Line 87: Indentation over 4 spaces
  `db.session.remove()`
- Line 88: Indentation over 4 spaces
  `db.drop_all()`
- Line 89: Indentation over 4 spaces
  `self.app_context.pop()`
- Line 90: Indentation over 4 spaces
  ``
- Line 91: Indentation over 4 spaces
  `def test_index_route(self):`
- Line 92: Indentation over 4 spaces
  `"""Test the main cabal index route"""`
- Line 93: Indentation over 4 spaces
  `response = self.client.get('/cabal/')`
- Line 94: Indentation over 4 spaces
  `self.assertEqual(response.status_code, 200)`
- Line 95: Indentation over 4 spaces
  `self.assertIn(b'Test Cabal', response.data)`
- Line 96: Indentation over 4 spaces
  ``
- Line 97: Indentation over 4 spaces
  `def test_create_cabal(self):`
- Line 98: Indentation over 4 spaces
  `"""Test creating a cabal"""`
- Line 99: Indentation over 4 spaces
  `# First, remove current cabal membership`
- Line 100: Indentation over 4 spaces
  `CabalMember.query.filter_by(chad_id=self.chad.id).delete()`
- Line 101: Indentation over 4 spaces
  `db.session.delete(self.cabal)`
- Line 102: Indentation over 4 spaces
  `db.session.commit()`
- Line 103: Indentation over 4 spaces
  ``
- Line 104: Indentation over 4 spaces
  `response = self.client.post('/cabal/create', data={`
- Line 105: Indentation over 4 spaces
  `'name': 'New Test Cabal',`
- Line 106: Indentation over 4 spaces
  `'description': 'A new test cabal description'`
- Line 107: Indentation over 4 spaces
  `}, follow_redirects=True)`
- Line 108: Indentation over 4 spaces
  ``
- Line 109: Indentation over 4 spaces
  `self.assertEqual(response.status_code, 200)`
- Line 110: Indentation over 4 spaces
  `self.assertIn(b'Cabal created successfully', response.data)`
- Line 111: Indentation over 4 spaces
  `self.assertIn(b'New Test Cabal', response.data)`
- Line 112: Indentation over 4 spaces
  ``
- Line 113: Indentation over 4 spaces
  `# Check database`
- Line 114: Indentation over 4 spaces
  `cabal = Cabal.query.filter_by(name='New Test Cabal').first()`
- Line 115: Indentation over 4 spaces
  `self.assertIsNotNone(cabal)`
- Line 116: Indentation over 4 spaces
  `self.assertEqual(cabal.leader_id, self.chad.id)`
- Line 117: Indentation over 4 spaces
  `self.assertEqual(cabal.member_count, 1)`
- Line 118: Indentation over 4 spaces
  ``
- Line 119: Indentation over 4 spaces
  `def test_appoint_officer(self):`
- Line 120: Indentation over 4 spaces
  `"""Test appointing an officer"""`
- Line 121: Indentation over 4 spaces
  `# Add another member to the cabal`
- Line 122: Indentation over 4 spaces
  `self.cabal.add_member(self.other_chads[0].id)`
- Line 123: Indentation over 4 spaces
  ``
- Line 124: Indentation over 4 spaces
  `response = self.client.post(f'/cabal/{self.cabal.id}/appoint_officer', data={`
- Line 125: Indentation over 4 spaces
  `'chad_id': self.other_chads[0].id,`
- Line 126: Indentation over 4 spaces
  `'role_type': 'clout'`
- Line 127: Indentation over 4 spaces
  `}, follow_redirects=True)`
- Line 128: Indentation over 4 spaces
  ``
- Line 129: Indentation over 4 spaces
  `self.assertEqual(response.status_code, 200)`
- Line 130: Indentation over 4 spaces
  `self.assertIn(b'Member appointed as Clout Commander', response.data)`
- Line 131: Indentation over 4 spaces
  ``
- Line 132: Indentation over 4 spaces
  `# Check database`
- Line 133: Indentation over 4 spaces
  `officer = self.cabal.get_officer('clout')`
- Line 134: Indentation over 4 spaces
  `self.assertIsNotNone(officer)`
- Line 135: Indentation over 4 spaces
  `self.assertEqual(officer.chad_id, self.other_chads[0].id)`
- Line 136: Indentation over 4 spaces
  ``
- Line 137: Indentation over 4 spaces
  `def test_remove_officer(self):`
- Line 138: Indentation over 4 spaces
  `"""Test removing an officer"""`
- Line 139: Indentation over 4 spaces
  `# Add another member and make them an officer`
- Line 140: Indentation over 4 spaces
  `self.cabal.add_member(self.other_chads[0].id)`
- Line 141: Indentation over 4 spaces
  `self.cabal.appoint_officer(self.other_chads[0].id, 'clout')`
- Line 142: Indentation over 4 spaces
  ``
- Line 143: Indentation over 4 spaces
  `response = self.client.get(f'/cabal/{self.cabal.id}/remove_officer/clout', follow_redirects=True)`
- Line 144: Indentation over 4 spaces
  ``
- Line 145: Indentation over 4 spaces
  `self.assertEqual(response.status_code, 200)`
- Line 146: Indentation over 4 spaces
  `self.assertIn(b'Officer removed from clout role', response.data)`
- Line 147: Indentation over 4 spaces
  ``
- Line 148: Indentation over 4 spaces
  `# Check database`
- Line 149: Indentation over 4 spaces
  `officer = self.cabal.get_officer('clout')`
- Line 150: Indentation over 4 spaces
  `self.assertIsNone(officer)`
- Line 151: Indentation over 4 spaces
  ``
- Line 152: Indentation over 4 spaces
  `def test_schedule_battle(self):`
- Line 153: Indentation over 4 spaces
  `"""Test scheduling a battle"""`
- Line 154: Indentation over 4 spaces
  `# Create another cabal to battle against`
- Line 155: Indentation over 4 spaces
  `other_cabal = Cabal(`
- Line 156: Indentation over 4 spaces
  `name="Opponent Cabal",`
- Line 157: Indentation over 4 spaces
  `description="An opponent cabal",`
- Line 158: Indentation over 4 spaces
  `leader_id=self.other_chads[0].id`
- Line 159: Indentation over 4 spaces
  `)`
- Line 160: Indentation over 4 spaces
  `db.session.add(other_cabal)`
- Line 161: Indentation over 4 spaces
  `db.session.commit()`
- Line 162: Indentation over 4 spaces
  ``
- Line 163: Indentation over 4 spaces
  `tomorrow = datetime.utcnow() + timedelta(days=1)`
- Line 164: Indentation over 4 spaces
  `date_str = tomorrow.strftime('%Y-%m-%d')`
- Line 165: Indentation over 4 spaces
  `time_str = tomorrow.strftime('%H:%M')`
- Line 166: Indentation over 4 spaces
  ``
- Line 167: Indentation over 4 spaces
  `response = self.client.post(f'/cabal/{self.cabal.id}/schedule_battle', data={`
- Line 168: Indentation over 4 spaces
  `'opponent_cabal_id': other_cabal.id,`
- Line 169: Indentation over 4 spaces
  `'battle_date': date_str,`
- Line 170: Indentation over 4 spaces
  `'battle_time': time_str`
- Line 171: Indentation over 4 spaces
  `}, follow_redirects=True)`
- Line 172: Indentation over 4 spaces
  ``
- Line 173: Indentation over 4 spaces
  `self.assertEqual(response.status_code, 200)`
- Line 174: Indentation over 4 spaces
  `self.assertIn(b'Battle scheduled successfully', response.data)`
- Line 175: Indentation over 4 spaces
  ``
- Line 176: Indentation over 4 spaces
  `# Check database`
- Line 177: Indentation over 4 spaces
  `battle = CabalBattle.query.filter_by(cabal_id=self.cabal.id).first()`
- Line 178: Indentation over 4 spaces
  `self.assertIsNotNone(battle)`
- Line 179: Indentation over 4 spaces
  `self.assertEqual(battle.opponent_cabal_id, other_cabal.id)`
- Line 180: Indentation over 4 spaces
  ``
- Line 181: Indentation over 4 spaces
  `def test_opt_into_battle(self):`
- Line 182: Indentation over 4 spaces
  `"""Test opting into a battle"""`
- Line 183: Indentation over 4 spaces
  `# Create a battle`
- Line 184: Indentation over 4 spaces
  `battle = CabalBattle(`
- Line 185: Indentation over 4 spaces
  `cabal_id=self.cabal.id,`
- Line 186: Indentation over 4 spaces
  `opponent_cabal_id=None,`
- Line 187: Indentation over 4 spaces
  `scheduled_at=datetime.utcnow() + timedelta(days=1),`
- Line 188: Indentation over 4 spaces
  `week_number=CabalBattle.get_current_week_number()`
- Line 189: Indentation over 4 spaces
  `)`
- Line 190: Indentation over 4 spaces
  `db.session.add(battle)`
- Line 191: Indentation over 4 spaces
  `db.session.commit()`
- Line 192: Indentation over 4 spaces
  ``
- Line 193: Indentation over 4 spaces
  `response = self.client.get(f'/cabal/battle/{battle.id}/opt_in', follow_redirects=True)`
- Line 194: Indentation over 4 spaces
  ``
- Line 195: Indentation over 4 spaces
  `self.assertEqual(response.status_code, 200)`
- Line 196: Indentation over 4 spaces
  `self.assertIn(b'Successfully opted into battle', response.data)`
- Line 197: Indentation over 4 spaces
  ``
- Line 198: Indentation over 4 spaces
  `# Check database`
- Line 199: Indentation over 4 spaces
  `member = CabalMember.query.filter_by(chad_id=self.chad.id).first()`
- Line 200: Indentation over 4 spaces
  `self.assertEqual(member.daily_battles, 1)`
- Line 201: Indentation over 4 spaces
  `self.assertEqual(member.battles_participated, 1)`
- Line 202: Indentation over 4 spaces
  ``
- Line 203: Indentation over 4 spaces
  `def test_vote_remove_leader(self):`
- Line 204: Indentation over 4 spaces
  `"""Test voting to remove a leader"""`
- Line 205: Indentation over 4 spaces
  `# Add another member`
- Line 206: Indentation over 4 spaces
  `self.cabal.add_member(self.other_chads[0].id)`
- Line 207: Indentation over 4 spaces
  ``
- Line 208: Indentation over 4 spaces
  `# Login as the other user`
- Line 209: Indentation over 4 spaces
  `with self.client.session_transaction() as session:`
- Line 210: Indentation over 4 spaces
  `session['_user_id'] = str(self.other_users[0].id)`
- Line 211: Indentation over 4 spaces
  ``
- Line 212: Indentation over 4 spaces
  `response = self.client.get(f'/cabal/{self.cabal.id}/vote_remove_leader', follow_redirects=True)`
- Line 213: Indentation over 4 spaces
  ``
- Line 214: Indentation over 4 spaces
  `self.assertEqual(response.status_code, 200)`
- Line 215: Indentation over 4 spaces
  `self.assertIn(b'Your vote to remove the leader has been recorded', response.data)`
- Line 216: Indentation over 4 spaces
  ``
- Line 217: Indentation over 4 spaces
  `# Check database`
- Line 218: Indentation over 4 spaces
  `vote_count = CabalVote.query.filter_by(`
- Line 219: Indentation over 4 spaces
  `cabal_id=self.cabal.id,`
- Line 220: Indentation over 4 spaces
  `vote_type='remove_leader',`
- Line 221: Indentation over 4 spaces
  `target_id=self.chad.id`
- Line 222: Indentation over 4 spaces
  `).count()`
- Line 223: Indentation over 4 spaces
  `self.assertEqual(vote_count, 1)`
- Line 224: Indentation over 4 spaces
  ``
- Line 225: Indentation over 4 spaces
  `def test_all_battles(self):`
- Line 226: Indentation over 4 spaces
  `"""Test viewing all battles"""`
- Line 227: Indentation over 4 spaces
  `# Create some battles`
- Line 228: Indentation over 4 spaces
  `for i in range(3):`
- Line 229: Indentation over 4 spaces
  `battle = CabalBattle(`
- Line 230: Indentation over 4 spaces
  `cabal_id=self.cabal.id,`
- Line 231: Indentation over 4 spaces
  `opponent_cabal_id=None,`
- Line 232: Indentation over 4 spaces
  `scheduled_at=datetime.utcnow() + timedelta(days=i+1),`
- Line 233: Indentation over 4 spaces
  `week_number=CabalBattle.get_current_week_number()`
- Line 234: Indentation over 4 spaces
  `)`
- Line 235: Indentation over 4 spaces
  `db.session.add(battle)`
- Line 236: Indentation over 4 spaces
  ``
- Line 237: Indentation over 4 spaces
  `# Add a completed battle`
- Line 238: Indentation over 4 spaces
  `past_battle = CabalBattle(`
- Line 239: Indentation over 4 spaces
  `cabal_id=self.cabal.id,`
- Line 240: Indentation over 4 spaces
  `opponent_cabal_id=None,`
- Line 241: Indentation over 4 spaces
  `scheduled_at=datetime.utcnow() - timedelta(days=1),`
- Line 242: Indentation over 4 spaces
  `completed=True,`
- Line 243: Indentation over 4 spaces
  `result='win',`
- Line 244: Indentation over 4 spaces
  `week_number=CabalBattle.get_current_week_number()`
- Line 245: Indentation over 4 spaces
  `)`
- Line 246: Indentation over 4 spaces
  `db.session.add(past_battle)`
- Line 247: Indentation over 4 spaces
  `db.session.commit()`
- Line 248: Indentation over 4 spaces
  ``
- Line 249: Indentation over 4 spaces
  `response = self.client.get('/cabal/battles')`
- Line 250: Indentation over 4 spaces
  ``
- Line 251: Indentation over 4 spaces
  `self.assertEqual(response.status_code, 200)`
- Line 252: Indentation over 4 spaces
  `self.assertIn(b'Upcoming Battles', response.data)`
- Line 253: Indentation over 4 spaces
  `self.assertIn(b'Past Battles', response.data)`
- Line 254: Indentation over 4 spaces
  ``
- Line 255: Indentation over 4 spaces
  `def test_leaderboard(self):`
- Line 256: Indentation over 4 spaces
  `"""Test cabal leaderboard"""`
- Line 257: Indentation over 4 spaces
  `# Create multiple cabals with different power levels`
- Line 258: Indentation over 4 spaces
  `for i in range(3):`
- Line 259: Indentation over 4 spaces
  `cabal = Cabal(`
- Line 260: Indentation over 4 spaces
  `name=f"Leaderboard Test Cabal {i}",`
- Line 261: Indentation over 4 spaces
  `description="A test cabal for leaderboard",`
- Line 262: Indentation over 4 spaces
  `leader_id=self.other_chads[i].id,`
- Line 263: Indentation over 4 spaces
  `total_power=1000 * (i + 1)`
- Line 264: Indentation over 4 spaces
  `)`
- Line 265: Indentation over 4 spaces
  `db.session.add(cabal)`
- Line 266: Indentation over 4 spaces
  `db.session.commit()`
- Line 267: Indentation over 4 spaces
  ``
- Line 268: Indentation over 4 spaces
  `response = self.client.get('/cabal/leaderboard')`
- Line 269: Indentation over 4 spaces
  ``
- Line 270: Indentation over 4 spaces
  `self.assertEqual(response.status_code, 200)`
- Line 271: Indentation over 4 spaces
  `self.assertIn(b'Cabal Leaderboard', response.data)`
- Line 272: Indentation over 4 spaces
  `self.assertIn(b'Leaderboard Test Cabal 2', response.data)  # Highest power should be listed`
- Line 273: Indentation over 4 spaces
  ``
- Line 274: Indentation over 4 spaces
  `def test_disband_cabal(self):`
- Line 275: Indentation over 4 spaces
  `"""Test disbanding a cabal"""`
- Line 276: Indentation over 4 spaces
  `cabal_id = self.cabal.id`
- Line 277: Indentation over 4 spaces
  ``
- Line 278: Indentation over 4 spaces
  `response = self.client.get(f'/cabal/{cabal_id}/disband', follow_redirects=True)`
- Line 279: Indentation over 4 spaces
  ``
- Line 280: Indentation over 4 spaces
  `self.assertEqual(response.status_code, 200)`
- Line 281: Indentation over 4 spaces
  `self.assertIn(b'Cabal disbanded successfully', response.data)`
- Line 282: Indentation over 4 spaces
  ``
- Line 283: Indentation over 4 spaces
  `# Check database`
- Line 284: Indentation over 4 spaces
  `self.assertIsNone(Cabal.query.get(cabal_id))`
- Line 285: Indentation over 4 spaces
  `self.assertEqual(CabalMember.query.filter_by(cabal_id=cabal_id).count(), 0)`
- Line 288: Indentation over 4 spaces
  `unittest.main()`

### tests\test_cabal_simplified.py (137 issues)

#### Code Smells
- Line 23: Explicit commit - check transaction management
  `db.session.commit()`
- Line 39: Explicit commit - check transaction management
  `db.session.commit()`
- Line 62: Explicit commit - check transaction management
  `db.session.commit()`
- Line 87: Explicit commit - check transaction management
  `db.session.commit()`
- Line 111: Explicit commit - check transaction management
  `db.session.commit()`

#### Best Practice Violations
- Line 8: Function without docstring
  `def setUp(self):`
- Line 25: Function without docstring
  `def tearDown(self):`
- Line 31: Function without docstring
  `def test_cabal_creation(self):`
- Line 54: Function without docstring
  `def test_add_member(self):`
- Line 79: Function without docstring
  `def test_remove_member(self):`
- Line 103: Function without docstring
  `def test_appoint_officer(self):`
- Line 11: Self assignment in method/constructor
  `self.app_context = self.app.app_context()`
- Line 8: Indentation over 4 spaces
  `def setUp(self):`
- Line 9: Indentation over 4 spaces
  `"""Set up test environment before each test"""`
- Line 10: Indentation over 4 spaces
  `self.app = create_app('testing')`
- Line 11: Indentation over 4 spaces
  `self.app_context = self.app.app_context()`
- Line 12: Indentation over 4 spaces
  `self.app_context.push()`
- Line 13: Indentation over 4 spaces
  ``
- Line 14: Indentation over 4 spaces
  `# Create a simplified database schema for testing`
- Line 15: Indentation over 4 spaces
  `db.create_all()`
- Line 16: Indentation over 4 spaces
  ``
- Line 17: Indentation over 4 spaces
  `# Create test data directly in the database`
- Line 18: Indentation over 4 spaces
  `self.test_chad_ids = []`
- Line 19: Indentation over 4 spaces
  `for i in range(5):`
- Line 20: Indentation over 4 spaces
  `chad_id = str(uuid.uuid4())`
- Line 21: Indentation over 4 spaces
  `self.test_chad_ids.append(chad_id)`
- Line 22: Indentation over 4 spaces
  ``
- Line 23: Indentation over 4 spaces
  `db.session.commit()`
- Line 24: Indentation over 4 spaces
  ``
- Line 25: Indentation over 4 spaces
  `def tearDown(self):`
- Line 26: Indentation over 4 spaces
  `"""Clean up after each test"""`
- Line 27: Indentation over 4 spaces
  `db.session.remove()`
- Line 28: Indentation over 4 spaces
  `db.drop_all()`
- Line 29: Indentation over 4 spaces
  `self.app_context.pop()`
- Line 30: Indentation over 4 spaces
  ``
- Line 31: Indentation over 4 spaces
  `def test_cabal_creation(self):`
- Line 32: Indentation over 4 spaces
  `"""Test basic cabal creation"""`
- Line 33: Indentation over 4 spaces
  `cabal = Cabal(`
- Line 34: Indentation over 4 spaces
  `name="Test Cabal",`
- Line 35: Indentation over 4 spaces
  `description="A test cabal",`
- Line 36: Indentation over 4 spaces
  `leader_id=self.test_chad_ids[0]`
- Line 37: Indentation over 4 spaces
  `)`
- Line 38: Indentation over 4 spaces
  `db.session.add(cabal)`
- Line 39: Indentation over 4 spaces
  `db.session.commit()`
- Line 40: Indentation over 4 spaces
  ``
- Line 41: Indentation over 4 spaces
  `# Check basic properties`
- Line 42: Indentation over 4 spaces
  `self.assertEqual(cabal.name, "Test Cabal")`
- Line 43: Indentation over 4 spaces
  `self.assertEqual(cabal.description, "A test cabal")`
- Line 44: Indentation over 4 spaces
  `self.assertEqual(cabal.leader_id, self.test_chad_ids[0])`
- Line 45: Indentation over 4 spaces
  `self.assertEqual(cabal.level, 1)`
- Line 46: Indentation over 4 spaces
  `self.assertEqual(cabal.xp, 0)`
- Line 47: Indentation over 4 spaces
  `self.assertTrue(cabal.invite_code)  # Should auto-generate`
- Line 48: Indentation over 4 spaces
  `self.assertEqual(cabal.member_count, 0)`
- Line 49: Indentation over 4 spaces
  ``
- Line 50: Indentation over 4 spaces
  `# Test invite code generation`
- Line 51: Indentation over 4 spaces
  `self.assertIsNotNone(cabal.invite_code)`
- Line 52: Indentation over 4 spaces
  `self.assertEqual(len(cabal.invite_code), 6)`
- Line 53: Indentation over 4 spaces
  ``
- Line 54: Indentation over 4 spaces
  `def test_add_member(self):`
- Line 55: Indentation over 4 spaces
  `"""Test adding members to a cabal"""`
- Line 56: Indentation over 4 spaces
  `cabal = Cabal(`
- Line 57: Indentation over 4 spaces
  `name="Member Test Cabal",`
- Line 58: Indentation over 4 spaces
  `description="Testing member functions",`
- Line 59: Indentation over 4 spaces
  `leader_id=self.test_chad_ids[0]`
- Line 60: Indentation over 4 spaces
  `)`
- Line 61: Indentation over 4 spaces
  `db.session.add(cabal)`
- Line 62: Indentation over 4 spaces
  `db.session.commit()`
- Line 63: Indentation over 4 spaces
  ``
- Line 64: Indentation over 4 spaces
  `# Add leader as member`
- Line 65: Indentation over 4 spaces
  `success, message = cabal.add_member(self.test_chad_ids[0])`
- Line 66: Indentation over 4 spaces
  `self.assertTrue(success)`
- Line 67: Indentation over 4 spaces
  `self.assertEqual(cabal.member_count, 1)`
- Line 68: Indentation over 4 spaces
  ``
- Line 69: Indentation over 4 spaces
  `# Add another member`
- Line 70: Indentation over 4 spaces
  `success, message = cabal.add_member(self.test_chad_ids[1])`
- Line 71: Indentation over 4 spaces
  `self.assertTrue(success)`
- Line 72: Indentation over 4 spaces
  `self.assertEqual(cabal.member_count, 2)`
- Line 73: Indentation over 4 spaces
  ``
- Line 74: Indentation over 4 spaces
  `# Try to add the same member again`
- Line 75: Indentation over 4 spaces
  `success, message = cabal.add_member(self.test_chad_ids[1])`
- Line 76: Indentation over 4 spaces
  `self.assertFalse(success)`
- Line 77: Indentation over 4 spaces
  `self.assertEqual(cabal.member_count, 2)`
- Line 78: Indentation over 4 spaces
  ``
- Line 79: Indentation over 4 spaces
  `def test_remove_member(self):`
- Line 80: Indentation over 4 spaces
  `"""Test removing members from a cabal"""`
- Line 81: Indentation over 4 spaces
  `cabal = Cabal(`
- Line 82: Indentation over 4 spaces
  `name="Remove Test Cabal",`
- Line 83: Indentation over 4 spaces
  `description="Testing removal functions",`
- Line 84: Indentation over 4 spaces
  `leader_id=self.test_chad_ids[0]`
- Line 85: Indentation over 4 spaces
  `)`
- Line 86: Indentation over 4 spaces
  `db.session.add(cabal)`
- Line 87: Indentation over 4 spaces
  `db.session.commit()`
- Line 88: Indentation over 4 spaces
  ``
- Line 89: Indentation over 4 spaces
  `# Add members`
- Line 90: Indentation over 4 spaces
  `cabal.add_member(self.test_chad_ids[0])`
- Line 91: Indentation over 4 spaces
  `cabal.add_member(self.test_chad_ids[1])`
- Line 92: Indentation over 4 spaces
  ``
- Line 93: Indentation over 4 spaces
  `# Try to remove the leader (should fail)`
- Line 94: Indentation over 4 spaces
  `success, message = cabal.remove_member(self.test_chad_ids[0])`
- Line 95: Indentation over 4 spaces
  `self.assertFalse(success)`
- Line 96: Indentation over 4 spaces
  `self.assertEqual(cabal.member_count, 2)`
- Line 97: Indentation over 4 spaces
  ``
- Line 98: Indentation over 4 spaces
  `# Remove a regular member`
- Line 99: Indentation over 4 spaces
  `success, message = cabal.remove_member(self.test_chad_ids[1])`
- Line 100: Indentation over 4 spaces
  `self.assertTrue(success)`
- Line 101: Indentation over 4 spaces
  `self.assertEqual(cabal.member_count, 1)`
- Line 102: Indentation over 4 spaces
  ``
- Line 103: Indentation over 4 spaces
  `def test_appoint_officer(self):`
- Line 104: Indentation over 4 spaces
  `"""Test appointing officers"""`
- Line 105: Indentation over 4 spaces
  `cabal = Cabal(`
- Line 106: Indentation over 4 spaces
  `name="Officer Test Cabal",`
- Line 107: Indentation over 4 spaces
  `description="Testing officer functions",`
- Line 108: Indentation over 4 spaces
  `leader_id=self.test_chad_ids[0]`
- Line 109: Indentation over 4 spaces
  `)`
- Line 110: Indentation over 4 spaces
  `db.session.add(cabal)`
- Line 111: Indentation over 4 spaces
  `db.session.commit()`
- Line 112: Indentation over 4 spaces
  ``
- Line 113: Indentation over 4 spaces
  `# Add members`
- Line 114: Indentation over 4 spaces
  `cabal.add_member(self.test_chad_ids[0])`
- Line 115: Indentation over 4 spaces
  `cabal.add_member(self.test_chad_ids[1])`
- Line 116: Indentation over 4 spaces
  ``
- Line 117: Indentation over 4 spaces
  `# Appoint an officer`
- Line 118: Indentation over 4 spaces
  `success, message = cabal.appoint_officer(self.test_chad_ids[1], 'clout')`
- Line 119: Indentation over 4 spaces
  `self.assertTrue(success)`
- Line 120: Indentation over 4 spaces
  ``
- Line 121: Indentation over 4 spaces
  `# Verify officer was appointed`
- Line 122: Indentation over 4 spaces
  `officer = cabal.get_officer('clout')`
- Line 123: Indentation over 4 spaces
  `self.assertIsNotNone(officer)`
- Line 124: Indentation over 4 spaces
  `self.assertEqual(officer.chad_id, self.test_chad_ids[1])`
- Line 125: Indentation over 4 spaces
  ``
- Line 126: Indentation over 4 spaces
  `# Try to appoint the leader (should fail)`
- Line 127: Indentation over 4 spaces
  `success, message = cabal.appoint_officer(self.test_chad_ids[0], 'roast_level')`
- Line 128: Indentation over 4 spaces
  `self.assertFalse(success)`
- Line 129: Indentation over 4 spaces
  ``
- Line 130: Indentation over 4 spaces
  `# Try to appoint invalid role`
- Line 131: Indentation over 4 spaces
  `success, message = cabal.appoint_officer(self.test_chad_ids[1], 'invalid_role')`
- Line 132: Indentation over 4 spaces
  `self.assertFalse(success)`

## Recommendations

### Security
- Review all SQL queries for potential injection risks
- Ensure all user inputs are validated and sanitized
- Add CSRF protection to all forms
- Review authentication checks in sensitive routes

### Code Quality
- Remove debug print statements
- Address TODOs and FIXMEs
- Improve exception handling - use specific exceptions
- Review database transaction management

### Best Practices
- Add docstrings to all functions and classes
- Standardize indentation and spacing
- Use more descriptive variable names where needed
- Add type hints to function parameters and return values

### Testing
- Increase test coverage for critical functionality
- Add integration tests for battle mechanics
- Add performance tests for power calculation
- Add security tests for leadership actions

