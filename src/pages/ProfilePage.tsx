import { useState, useEffect } from 'react';
import { 
  Mail, MapPin, Link2, BookOpen, FileText, Briefcase, 
  Award, ShieldCheck, Share2, Download, Edit3, ChevronRight, Activity, Save, X
} from 'lucide-react';
import { useAuthStore } from '../store/authStore';
import { api } from '../utils/api';
import { useToastStore } from '../store/toastStore';

export default function ProfilePage() {
  const { user, checkAuth } = useAuthStore();
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    name: user?.name || '',
    title: user?.title || '',
    institution: user?.institution || '',
    bio: user?.bio || '',
    location: user?.location || '',
    website: user?.website || '',
    orcid: user?.orcid || '',
    google_scholar: user?.google_scholar || ''
  });
  const [isSaving, setIsSaving] = useState(false);
  const { addToast } = useToastStore();

  // Re-sync local state when user from store updates
  useEffect(() => {
    if (user) {
      setFormData({
        name: user.name || '',
        title: user.title || '',
        institution: user.institution || '',
        bio: user.bio || '',
        location: user.location || '',
        website: user.website || '',
        orcid: user.orcid || '',
        google_scholar: user.google_scholar || ''
      });
    }
  }, [user]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      await api.auth.updateProfile(formData);
      await checkAuth(); // Refresh user data from backend
      addToast("Profile updated successfully", "success");
      setIsEditing(false);
    } catch (error) {
      console.error("Failed to update profile:", error);
      addToast("Failed to update profile", "error");
    } finally {
      setIsSaving(false);
    }
  };

  if (!user) {
    return <div className="flex h-full items-center justify-center p-8">Loading profile...</div>;
  }

  return (
    <div className="absolute inset-0 bg-[#FBFDFB] rounded-2xl border border-slate-200 shadow-sm overflow-y-auto font-sans">
      
      {/* HEADER */}
      <div className="h-48 bg-gradient-to-r from-emerald-600 to-teal-800 relative">
        <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
        <div className="absolute -bottom-12 left-8 md:left-12 flex items-end gap-6">
          <div className="w-28 h-28 rounded-2xl bg-white p-1.5 shadow-lg relative">
            <div className="w-full h-full bg-emerald-100 text-emerald-700 flex items-center justify-center text-4xl font-black rounded-xl uppercase">
              {user.name?.charAt(0) || 'R'}
            </div>
            <div className="absolute -bottom-2 -right-2 bg-blue-500 text-white w-8 h-8 flex items-center justify-center rounded-full border-2 border-white shadow-sm" title="Verified Researcher">
              <ShieldCheck className="w-4 h-4" />
            </div>
          </div>
        </div>
        {!isEditing && (
          <div className="absolute top-4 right-4 flex gap-2">
            <button className="px-4 py-2 bg-white/20 hover:bg-white/30 text-white backdrop-blur-md rounded-xl text-xs font-bold transition-colors flex items-center gap-2">
              <Share2 className="w-3.5 h-3.5" /> Share
            </button>
            <button className="px-4 py-2 bg-white/20 hover:bg-white/30 text-white backdrop-blur-md rounded-xl text-xs font-bold transition-colors flex items-center gap-2">
              <Download className="w-3.5 h-3.5" /> Export
            </button>
          </div>
        )}
      </div>

      <div className="pt-16 px-8 md:px-12 pb-12 max-w-6xl mx-auto flex flex-col lg:flex-row gap-12">
        
        {/* LEFT: INFO */}
        <div className="lg:w-1/3 space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-300">
          
          <div>
            <div className="flex items-start justify-between">
              <div className="w-full">
                {isEditing ? (
                  <div className="space-y-3">
                    <input name="name" value={formData.name} onChange={handleChange} placeholder="Full Name" className="w-full text-xl font-black text-slate-900 border-b border-slate-300 focus:border-emerald-500 outline-none pb-1 bg-transparent" />
                    <input name="title" value={formData.title} onChange={handleChange} placeholder="Title (e.g. Postdoctoral Researcher)" className="w-full text-[13px] font-bold text-emerald-600 uppercase tracking-widest border-b border-slate-300 focus:border-emerald-500 outline-none pb-1 bg-transparent" />
                    <input name="institution" value={formData.institution} onChange={handleChange} placeholder="Institution" className="w-full text-sm font-semibold text-slate-500 border-b border-slate-300 focus:border-emerald-500 outline-none pb-1 bg-transparent" />
                  </div>
                ) : (
                  <div>
                    <h1 className="text-2xl font-black text-slate-900 leading-tight">{user.name}</h1>
                    {user.title && <p className="text-[13px] font-bold text-emerald-600 mt-1 uppercase tracking-widest">{user.title}</p>}
                    {user.institution && <p className="text-sm font-semibold text-slate-500 mt-0.5">{user.institution}</p>}
                  </div>
                )}
              </div>
              
              {!isEditing ? (
                <button onClick={() => setIsEditing(true)} className="p-2 ml-4 text-slate-400 hover:text-emerald-600 hover:bg-emerald-50 rounded-lg transition-colors border border-slate-200 shadow-sm shrink-0" title="Edit Profile">
                  <Edit3 className="w-4 h-4" />
                </button>
              ) : (
                <div className="flex gap-2 ml-4">
                  <button onClick={() => setIsEditing(false)} className="p-2 text-slate-400 hover:bg-slate-100 rounded-lg transition-colors">
                    <X className="w-4 h-4" />
                  </button>
                  <button onClick={handleSave} disabled={isSaving} className="p-2 text-emerald-600 hover:bg-emerald-50 rounded-lg transition-colors disabled:opacity-50">
                    <Save className="w-4 h-4" />
                  </button>
                </div>
              )}
            </div>
            
            {isEditing ? (
              <textarea name="bio" value={formData.bio} onChange={handleChange} placeholder="Bio..." rows={4} className="w-full text-sm text-slate-600 font-medium leading-relaxed mt-4 border border-slate-300 focus:border-emerald-500 rounded-lg p-2 outline-none resize-none" />
            ) : (
              user.bio && <p className="text-sm text-slate-600 font-medium leading-relaxed mt-4">{user.bio}</p>
            )}
          </div>

          <div className="space-y-3 pt-6 border-t border-slate-100">
            <div className="flex items-center gap-3 text-sm font-medium text-slate-600">
              <Mail className="w-4 h-4 text-slate-400 shrink-0" /> {user.email}
            </div>
            
            {isEditing ? (
              <div className="flex items-center gap-3 text-sm font-medium text-slate-600">
                <MapPin className="w-4 h-4 text-slate-400 shrink-0" />
                <input name="location" value={formData.location} onChange={handleChange} placeholder="Location" className="w-full border-b border-slate-300 focus:border-emerald-500 outline-none bg-transparent" />
              </div>
            ) : (
              user.location && (
                <div className="flex items-center gap-3 text-sm font-medium text-slate-600">
                  <MapPin className="w-4 h-4 text-slate-400 shrink-0" /> {user.location}
                </div>
              )
            )}
            
            {isEditing ? (
              <div className="flex items-center gap-3 text-sm font-medium text-slate-600">
                <Link2 className="w-4 h-4 text-slate-400 shrink-0" />
                <input name="website" value={formData.website} onChange={handleChange} placeholder="Website URL" className="w-full border-b border-slate-300 focus:border-emerald-500 outline-none bg-transparent" />
              </div>
            ) : (
              user.website && (
                <div className="flex items-center gap-3 text-sm font-medium text-slate-600">
                  <Link2 className="w-4 h-4 text-slate-400 shrink-0" /> <a href={user.website} target="_blank" rel="noreferrer" className="hover:text-emerald-600 underline">{user.website}</a>
                </div>
              )
            )}
          </div>

          <div className="pt-6 border-t border-slate-100 space-y-4">
            <h3 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">External Profiles</h3>
            
            {isEditing ? (
              <div className="space-y-3">
                <div>
                  <label className="text-xs font-bold text-slate-500">ORCID</label>
                  <input name="orcid" value={formData.orcid} onChange={handleChange} placeholder="0000-0000-0000-0000" className="w-full border border-slate-300 rounded-lg px-3 py-1.5 text-sm mt-1 focus:border-emerald-500 outline-none" />
                </div>
                <div>
                  <label className="text-xs font-bold text-slate-500">Google Scholar URL</label>
                  <input name="google_scholar" value={formData.google_scholar} onChange={handleChange} placeholder="https://scholar.google.com/..." className="w-full border border-slate-300 rounded-lg px-3 py-1.5 text-sm mt-1 focus:border-emerald-500 outline-none" />
                </div>
              </div>
            ) : (
              <div className="space-y-2">
                {user.orcid && (
                  <button className="w-full flex items-center justify-between px-4 py-2.5 bg-slate-50 hover:bg-slate-100 text-slate-700 rounded-xl border border-slate-200 transition-colors text-xs font-bold">
                    <span className="flex items-center gap-2">ORCID</span>
                    <span className="text-slate-400 font-medium">{user.orcid}</span>
                  </button>
                )}
                {user.google_scholar && (
                  <button onClick={() => window.open(user.google_scholar, '_blank')} className="w-full flex items-center justify-between px-4 py-2.5 bg-slate-50 hover:bg-slate-100 text-slate-700 rounded-xl border border-slate-200 transition-colors text-xs font-bold">
                    <span className="flex items-center gap-2">Google Scholar</span>
                    <ChevronRight className="w-4 h-4 text-slate-400" />
                  </button>
                )}
                {!user.orcid && !user.google_scholar && (
                  <p className="text-xs text-slate-400 italic">No external profiles added.</p>
                )}
              </div>
            )}
          </div>

        </div>

        {/* RIGHT: STATS & ACTIVITY */}
        <div className="lg:w-2/3 space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-500">
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white border border-slate-200 p-5 rounded-2xl shadow-sm">
              <div className="flex items-center gap-2 mb-2">
                <BookOpen className="w-4 h-4 text-emerald-500" />
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Library</span>
              </div>
              <span className="text-2xl font-black text-slate-800">{user.stats?.papers_saved ?? 0}</span>
              <p className="text-[10px] font-semibold text-slate-500 mt-1">Papers saved</p>
            </div>
            <div className="bg-white border border-slate-200 p-5 rounded-2xl shadow-sm">
              <div className="flex items-center gap-2 mb-2">
                <Briefcase className="w-4 h-4 text-blue-500" />
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Projects</span>
              </div>
              <span className="text-2xl font-black text-slate-800">{user.stats?.projects_active ?? 0}</span>
              <p className="text-[10px] font-semibold text-slate-500 mt-1">Active research</p>
            </div>
            <div className="bg-white border border-slate-200 p-5 rounded-2xl shadow-sm">
              <div className="flex items-center gap-2 mb-2">
                <FileText className="w-4 h-4 text-purple-500" />
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Notes</span>
              </div>
              <span className="text-2xl font-black text-slate-800">{user.stats?.notes_written ?? 0}</span>
              <p className="text-[10px] font-semibold text-slate-500 mt-1">Written notes</p>
            </div>
            <div className="bg-white border border-slate-200 p-5 rounded-2xl shadow-sm opacity-50">
              <div className="flex items-center gap-2 mb-2">
                <Award className="w-4 h-4 text-amber-500" />
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Streak</span>
              </div>
              <span className="text-xl font-bold text-slate-400">—</span>
              <p className="text-[10px] font-semibold text-slate-400 mt-1">Unavailable</p>
            </div>
          </div>

          <div>
            <h3 className="text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-4 flex items-center gap-2">
              <Activity className="w-4 h-4" /> Recent Activity
            </h3>
            <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-4 text-sm text-slate-500 italic text-center">
              No recent activity recorded yet.
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
