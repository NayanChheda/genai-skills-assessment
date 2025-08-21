# challenges/level_1_basic/validate_git_tasks.py
import subprocess
import re
from pathlib import Path
from typing import Tuple, List, Dict, Any

def analyze_commit_messages() -> Tuple[float, str]:
    """
    Analyze commit messages for quality using relevant metrics only.
    
    Returns:
        tuple: (score, details) where score is 0-1 and details is a string
    """
    result = subprocess.run(
        'git log --oneline --format="%h|%s" -n 20',
        shell=True, capture_output=True, text=True
    )
    
    if not result.stdout.strip():
        return 0.0, "No commits found"
    
    commits: List[Dict[str, Any]] = []
    for line in result.stdout.strip().split('\n'):
        if '|' in line:
            commit_hash, message = line.split('|', 1)
            commits.append({
                'message': message.strip(),
                'length': len(message.strip()),
                'has_verb': bool(re.search(
                    r'^(add|fix|update|remove|refactor|implement|create|docs|test|style|chore|feat|perf|ci)',
                    message.lower()
                )),
                'is_meaningful': (
                    len(message.strip()) > 15 and 
                    not message.lower().startswith('merge') and 
                    not message.lower().startswith('wip') and
                    not message.lower().startswith('update') and
                    not message.lower().startswith('fix')
                )
            })
    
    total_commits = len(commits)
    if total_commits == 0:
        return 0.0, "No commits to analyze"
    
    # Calculate only relevant quality metrics
    meaningful_commits = sum(1 for c in commits if c['is_meaningful'])
    verb_commits = sum(1 for c in commits if c['has_verb'])
    avg_length = sum(c['length'] for c in commits) / total_commits
    
    # Weighted score with ONLY relevant metrics
    score = (
        (meaningful_commits / total_commits) * 0.6 +  # Most important: meaningful messages
        (verb_commits / total_commits) * 0.3 +        # Action-oriented messages
        (min(avg_length, 60) / 60) * 0.1             # Reasonable length (capped at 60 chars)
    )
    
    details = f"Meaningful commits: {meaningful_commits}/{total_commits}, Action-oriented: {verb_commits}/{total_commits}"
    return round(score, 2), details

def check_branch_structure() -> Tuple[float, str]:
    """
    Check if branching structure follows good practices - simplified.
    
    Returns:
        tuple: (score, details) where score is 0-1 and details is a string
    """
    result = subprocess.run(
        "git branch --format='%(refname:short)'",
        shell=True, capture_output=True, text=True
    )
    
    branches = [b.strip() for b in result.stdout.split('\n') if b.strip()]
    
    if not branches:
        return 0.0, "No branches found"
    
    # Check for main/master branch
    has_main_branch = any(b in ['main', 'master'] for b in branches)
    
    # Check for feature/development branches (not just main)
    has_feature_branches = len(branches) > 1 or any(
        b for b in branches 
        if b not in ['main', 'master'] and not b.startswith('HEAD')
    )
    
    # Scoring: 50% for having main branch, 50% for having other branches
    score = 0.5 if has_main_branch else 0.0
    score += 0.5 if has_feature_branches else 0.0
    
    details = f"Total branches: {len(branches)}, Has main: {has_main_branch}, Has features: {has_feature_branches}"
    return round(score, 2), details

def check_recent_activity() -> Tuple[float, str]:
    """
    Check for reasonable commit activity patterns.
    
    Returns:
        tuple: (score, details) where score is 0-1 and details is a string
    """
    result = subprocess.run(
        'git log --oneline --since="2 weeks ago"',
        shell=True, capture_output=True, text=True
    )
    
    recent_commits = [line for line in result.stdout.strip().split('\n') if line.strip()]
    commit_count = len(recent_commits)
    
    # Score based on having some recent activity (1-10+ commits in 2 weeks)
    if commit_count == 0:
        return 0.0, "No recent commits (last 2 weeks)"
    elif commit_count == 1:
        return 0.3, "Only 1 recent commit"
    else:
        score = min(commit_count / 10, 1.0)  # Max score at 10+ commits
        return round(score, 2), f"Recent commits: {commit_count}"

def main() -> bool:
    """
    Comprehensive Git practices assessment for candidate evaluation.
    
    Returns:
        bool: True if overall score meets minimum threshold
    """
    print("🔍 Comprehensive Git Practices Assessment")
    print("=" * 50)
    
    if not Path(".git").exists():
        print("❌ Not a git repository")
        return False
    
    try:
        # Calculate all Git quality metrics
        commit_score, commit_details = analyze_commit_messages()
        branch_score, branch_details = check_branch_structure()
        activity_score, activity_details = check_recent_activity()
        
        # Weighted overall score
        overall_score = (
            commit_score * 0.6 +  # Commit quality is most important (60%)
            branch_score * 0.3 +  # Branch structure (30%)
            activity_score * 0.1   # Recent activity (10%)
        )
        
        # Display detailed results
        print(f"\n📊 Commit Message Quality: {commit_score:.0%}")
        print(f"   {commit_details}")
        
        print(f"\n🌿 Branch Structure: {branch_score:.0%}")
        print(f"   {branch_details}")
        
        print(f"\n🕒 Recent Activity: {activity_score:.0%}")
        print(f"   {activity_details}")
        
        print(f"\n{'=' * 50}")
        print(f"✅ Overall Git Score: {overall_score:.1%}")
        
        # Provide actionable feedback
        if overall_score >= 0.8:
            print("🎉 Excellent Git practices!")
            return True
        elif overall_score >= 0.6:
            print("⚠️  Good Git practices - some room for improvement")
            return True
        elif overall_score >= 0.4:
            print("⚠️  Basic Git practices - needs improvement")
            return True
        else:
            print("❌ Poor Git practices - significant improvement needed")
            return False
            
    except Exception as e:
        print(f"❌ Assessment failed with error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)