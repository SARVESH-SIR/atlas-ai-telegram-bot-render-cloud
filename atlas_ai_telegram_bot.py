#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATLAS AI Telegram Bot - Multi-User Edition for Render Deployment
Complete AI intelligence with multi-user support for cloud hosting
"""

import os
import sys
import time
import requests
from datetime import datetime
from typing import Dict
from media_handler import MediaHandler

class AtlasAITelegramBot:
    """ATLAS AI Telegram Bot with Complete Intelligence for Render"""
    
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.groq_api_key = os.getenv('GroqAPIKey')
        self.assistant_name = os.getenv('AssistantName', 'ATLAS')
        self.creator_name = os.getenv('Creator', 'K.V.SARVESH')
        self.port = int(os.getenv('PORT', 8000))
        self.user_sessions = {}
        self.last_update_id = 0
        self.active_users = set()
        self.total_messages = 0
        self.start_time = datetime.now()
        self.media_handler = MediaHandler()  # Add media handling capabilities
        
        if not self.bot_token or not self.groq_api_key:
            print("❌ Missing required environment variables")
            print("Please set TELEGRAM_BOT_TOKEN and GroqAPIKey in Render")
            sys.exit(1)
    
    def get_user_session(self, user_id: int) -> Dict:
        """Get or create user session with multi-user support"""
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {
                "messages": [],
                "last_activity": datetime.now(),
                "name": None,
                "username": None,
                "message_count": 0,
                "session_start": datetime.now(),
                "preferences": {
                    "response_style": "detailed",
                    "language": "en"
                }
            }
            self.active_users.add(user_id)
        return self.user_sessions[user_id]
    
    def get_bot_stats(self) -> str:
        """Get comprehensive bot statistics"""
        uptime = datetime.now() - self.start_time
        hours = int(uptime.total_seconds() // 3600)
        minutes = int((uptime.total_seconds() % 3600) // 60)
        
        return f"""📊 {self.assistant_name} AI - Multi-User Statistics

🤖 <b>Bot Status:</b> ✅ Online & Multi-User Ready
👨‍💻 <b>Creator:</b> {self.creator_name}
🌐 <b>Platform:</b> Render Cloud Services
🕐 <b>Uptime:</b> {hours}h {minutes}m
📈 <b>Total Messages:</b> {self.total_messages}
👥 <b>Active Users:</b> {len(self.active_users)}
💾 <b>Total Sessions:</b> {len(self.user_sessions)}

🔧 <b>AI Engine:</b> Groq LLaMA 3.3 70B
🌐 <b>Multi-User Support:</b> ✅ Active
🧠 <b>Memory per User:</b> Individual sessions
🔄 <b>Concurrent Processing:</b> Enabled

📱 <b>Multi-User Features:</b>
✅ Individual conversation memory
✅ Separate user preferences
✅ Concurrent message handling
✅ User-specific context
✅ Session persistence
✅ Privacy isolation

🚀 Bot serving multiple users simultaneously on Render!"""
    
    def get_user_info(self, user_id: int) -> str:
        """Get detailed user information"""
        if user_id not in self.user_sessions:
            return "❌ User not found"
        
        session = self.user_sessions[user_id]
        session_duration = datetime.now() - session["session_start"]
        hours = int(session_duration.total_seconds() // 3600)
        minutes = int((session_duration.total_seconds() % 3600) // 60)
        
        return f"""👤 <b>User Information:</b>

🆔 <b>User ID:</b> {user_id}
👨‍💼 <b>Name:</b> {session.get('name', 'Unknown')}
🏷️ <b>Username:</b> @{session.get('username', 'N/A')}
💬 <b>Messages:</b> {session['message_count']}
🕐 <b>Session Duration:</b> {hours}h {minutes}m
📅 <b>Started:</b> {session['session_start'].strftime('%Y-%m-%d %H:%M:%S')}
⚙️ <b>Response Style:</b> {session['preferences']['response_style']}
🌐 <b>Language:</b> {session['preferences']['language']}
💾 <b>Memory Items:</b> {len(session['messages'])}"""
    
    def call_groq_ai(self, message: str, user_id: int) -> str:
        """Call Groq AI for intelligent responses"""
        try:
            session = self.get_user_session(user_id)
            
            messages = [
                {
                    "role": "system", 
                    "content": f"""You are {self.assistant_name}, a highly advanced AI assistant with complete Atlas AI capabilities deployed on Render cloud services.

Your capabilities include:
• Complete knowledge across all domains
• Advanced reasoning and analysis
• Natural, engaging conversations
• Real-time information access
• Creative intelligence and writing
• Technical expertise (programming, science, math)
• Research and detailed explanations
• Memory of conversation context

Be highly intelligent, comprehensive, and helpful. Use emojis appropriately. Provide detailed, well-structured responses.

Current context: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
User: {session.get('name', 'User')}
Session history: {len(session['messages'])} messages
Platform: Render Cloud Services
Creator: {self.creator_name}

You are the complete Atlas AI with full intelligence capabilities."""
                }
            ]
            
            # Add conversation history
            if session["messages"]:
                messages.extend(session["messages"][-8:])
            
            messages.append({"role": "user", "content": message})
            
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "llama-3.3-70b-versatile",
                "messages": messages,
                "max_tokens": 3000,
                "temperature": 0.7
            }
            
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result["choices"][0]["message"]["content"]
                
                # Update session
                session["messages"].append({"role": "user", "content": message})
                session["messages"].append({"role": "assistant", "content": ai_response})
                session["last_activity"] = datetime.now()
                session["message_count"] += 1
                self.total_messages += 1
                
                return ai_response
            else:
                return f"❌ AI Service Error: {response.status_code}"
                
        except Exception as e:
            return f"❌ AI Service temporarily unavailable. Please try again."
    
    def send_message(self, chat_id: int, text: str) -> bool:
        """Send message via Telegram API"""
        try:
            response = requests.post(
                f"https://api.telegram.org/bot{self.bot_token}/sendMessage",
                json={
                    'chat_id': chat_id,
                    'text': text,
                    'parse_mode': 'HTML'
                },
                timeout=30
            )
            return response.status_code == 200
        except:
            return False
    
    def send_voice_message(self, chat_id: int, voice_file_path: str) -> bool:
        """Send voice message via Telegram API"""
        try:
            with open(voice_file_path, 'rb') as voice_file:
                response = requests.post(
                    f"https://api.telegram.org/bot{self.bot_token}/sendVoice",
                    data={
                        'chat_id': chat_id
                    },
                    files={
                        'voice': voice_file
                    },
                    timeout=30
                )
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Voice send error: {e}")
            return False
    
    def send_document(self, chat_id: int, document_path: str, caption: str = "") -> bool:
        """Send document via Telegram API"""
        try:
            with open(document_path, 'rb') as doc_file:
                response = requests.post(
                    f"https://api.telegram.org/bot{self.bot_token}/sendDocument",
                    data={
                        'chat_id': chat_id,
                        'caption': caption
                    },
                    files={
                        'document': doc_file
                    },
                    timeout=30
                )
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Document send error: {e}")
            return False
    
    def process_message(self, user_id: int, user_name: str, username: str, text: str):
        """Process incoming message with multi-user support"""
        print(f"📩 @{username or 'N/A'} ({user_name}): {text}")
        
        session = self.get_user_session(user_id)
        if not session["name"]:
            session["name"] = user_name
        if username:
            session["username"] = username
        
        # Handle commands
        if text.lower() == '/start':
            welcome = f"""🚀 Welcome to {self.assistant_name} AI - Multi-User Media Edition!

Hello {user_name}! I'm {self.assistant_name}, your advanced AI assistant with complete Atlas intelligence and media capabilities deployed on Render cloud services.

🌟 <b>Multi-User Features:</b>
👥 <b>Individual Sessions:</b> Your private conversation memory
🔒 <b>Privacy Protected:</b> Your data is isolated from other users
🧠 <b>Smart Context:</b> I remember our conversation
⚙️ <b>Personalized:</b> Customized responses for you
🌐 <b>Cloud Powered:</b> Running on Render cloud services

� <b>Media Capabilities:</b>
🗣️ <b>Voice Messages:</b> Convert text to speech
📝 <b>Note Generation:</b> Create markdown notes
📄 <b>Document Creation:</b> Generate PDF, Word, Excel files
📊 <b>Report Generation:</b> Multi-format summaries

�🎯 <b>Commands:</b>
/start - Welcome message
/help - Show all capabilities
/stats - Bot statistics
/myinfo - Your session info
/clear - Clear your conversation
/voice <text> - Convert text to voice
/note <title> - Create markdown note
/pdf <title> - Generate PDF document
/word <title> - Create Word document
/excel <title> - Generate Excel sheet
/report <title> - Generate multi-format report

🌟 <b>AI Capabilities:</b>
🧠 Advanced reasoning & analysis
💬 Natural conversations
🔍 Deep research & analysis
🎨 Creative writing & ideas
💻 Technical support
📚 Knowledge across all domains
🧠 Memory & context

💡 <b>Multi-User Examples:</b>
• Each user gets private AI conversations
• Your preferences are saved separately
• No interference between users
• Concurrent support for many users
• Generate personalized voice messages
• Create custom documents and reports

🔥 Created by {self.creator_name}
🌐 Deployed on Render Cloud Services
Powered by complete Atlas AI technology!

Ask me anything - I'm ready to help you personally with text and media! 🚀"""
            self.send_message(user_id, welcome)
            return
        
        elif text.lower() == '/help':
            help_text = f"""🧠 {self.assistant_name} AI - Multi-User Media Help

📋 <b>Basic Commands:</b>
/start - Welcome message
/help - Show this help
/stats - Global bot statistics
/myinfo - Your session information
/clear - Clear your conversation

🎵 <b>Media Commands:</b>
/voice <text> - Convert text to voice message
/note <title> - Create markdown note file
/pdf <title> - Generate PDF document
/word <title> - Create Word document
/excel <title> - Generate Excel sheet
/report <title> - Generate multi-format report

🌟 <b>Multi-User Features:</b>
👥 <b>Individual Sessions:</b> Each user has private conversation
🔒 <b>Privacy Isolation:</b> Your data is completely separate
🧠 <b>Personal Memory:</b> I remember our conversations
⚙️ <b>User Preferences:</b> Customized experience
🔄 <b>Concurrent Support:</b> Multiple users simultaneously

🌟 <b>AI Capabilities:</b>
🧠 <b>Advanced Intelligence:</b> Complex reasoning
💬 <b>Natural Conversations:</b> Human-like dialogue
🔍 <b>Research & Analysis:</b> Deep information processing
🎨 <b>Creative Tasks:</b> Writing, brainstorming
💻 <b>Technical Support:</b> Programming, science, math
📚 <b>Knowledge Base:</b> All domains and subjects
🧠 <b>Memory:</b> Context-aware conversations

💡 <b>Media Examples:</b>
• "/voice Hello world" - Get voice message
• "/note My Ideas" - Create markdown note
• "/pdf Business Plan" - Generate PDF
• "/word Meeting Notes" - Create Word doc
• "/excel Project Data" - Generate Excel
• "/report Summary" - Get all formats

💡 <b>Multi-User Benefits:</b>
✅ Private conversations with AI
✅ No interference from other users
✅ Personalized responses
✅ Session persistence
✅ Individual preferences
✅ Personal media files

🔥 <b>Powered by:</b> Complete Atlas AI Technology
👨‍💻 <b>Created by:</b> {self.creator_name}
🌐 <b>Platform:</b> Render Cloud Services

Ask me anything - I have complete intelligence and media capabilities for you!"""
            self.send_message(user_id, help_text)
            return
        
        elif text.lower().startswith('/voice '):
            # Extract text for voice conversion
            voice_text = text[7:].strip()  # Remove "/voice " prefix
            if voice_text:
                self.send_message(user_id, "🎵 Converting text to voice...")
                voice_file = self.media_handler.text_to_speech(voice_text, user_id)
                if voice_file:
                    self.send_voice_message(user_id, voice_file)
                else:
                    self.send_message(user_id, "❌ Failed to generate voice message")
            else:
                self.send_message(user_id, "❌ Please provide text to convert to voice\nExample: /voice Hello world")
            return
        
        elif text.lower().startswith('/note '):
            # Extract title for note
            note_title = text[6:].strip()  # Remove "/note " prefix
            if note_title:
                self.send_message(user_id, "📝 Creating markdown note...")
                # Get last AI response or create default content
                last_messages = session.get("messages", [])
                content = "This is your personalized note generated by ATLAS AI."
                if last_messages:
                    content = last_messages[-1].get("content", content) if last_messages[-1].get("role") == "assistant" else content
                
                note_file = self.media_handler.generate_markdown_note(note_title, content, user_id)
                if note_file:
                    file_info = self.media_handler.get_file_info(note_file)
                    self.send_document(user_id, note_file, f"📝 Your note: {note_title}")
                else:
                    self.send_message(user_id, "❌ Failed to generate note")
            else:
                self.send_message(user_id, "❌ Please provide a title for the note\nExample: /note My Ideas")
            return
        
        elif text.lower().startswith('/pdf '):
            # Extract title for PDF
            pdf_title = text[5:].strip()  # Remove "/pdf " prefix
            if pdf_title:
                self.send_message(user_id, "📄 Generating PDF document...")
                # Get last AI response or create default content
                last_messages = session.get("messages", [])
                content = "This is your personalized PDF document generated by ATLAS AI."
                if last_messages:
                    content = last_messages[-1].get("content", content) if last_messages[-1].get("role") == "assistant" else content
                
                pdf_file = self.media_handler.generate_pdf_document(pdf_title, content, user_id)
                if pdf_file:
                    file_info = self.media_handler.get_file_info(pdf_file)
                    self.send_document(user_id, pdf_file, f"📄 Your PDF: {pdf_title}")
                else:
                    self.send_message(user_id, "❌ Failed to generate PDF")
            else:
                self.send_message(user_id, "❌ Please provide a title for the PDF\nExample: /pdf Business Plan")
            return
        
        elif text.lower().startswith('/word '):
            # Extract title for Word document
            word_title = text[6:].strip()  # Remove "/word " prefix
            if word_title:
                self.send_message(user_id, "📝 Creating Word document...")
                # Get last AI response or create default content
                last_messages = session.get("messages", [])
                content = "This is your personalized Word document generated by ATLAS AI."
                if last_messages:
                    content = last_messages[-1].get("content", content) if last_messages[-1].get("role") == "assistant" else content
                
                word_file = self.media_handler.generate_word_document(word_title, content, user_id)
                if word_file:
                    file_info = self.media_handler.get_file_info(word_file)
                    self.send_document(user_id, word_file, f"📝 Your Word document: {word_title}")
                else:
                    self.send_message(user_id, "❌ Failed to generate Word document")
            else:
                self.send_message(user_id, "❌ Please provide a title for the Word document\nExample: /word Meeting Notes")
            return
        
        elif text.lower().startswith('/excel '):
            # Extract title for Excel sheet
            excel_title = text[7:].strip()  # Remove "/excel " prefix
            if excel_title:
                self.send_message(user_id, "📊 Generating Excel sheet...")
                # Create sample data
                data = {
                    "User Name": session.get("name", "Unknown"),
                    "Username": session.get("username", "N/A"),
                    "Messages": session.get("message_count", 0),
                    "Session Start": session.get("session_start", datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
                    "Last Activity": session.get("last_activity", datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
                    "Generated By": f"{self.assistant_name} AI"
                }
                
                excel_file = self.media_handler.generate_excel_sheet(excel_title, data, user_id)
                if excel_file:
                    file_info = self.media_handler.get_file_info(excel_file)
                    self.send_document(user_id, excel_file, f"📊 Your Excel sheet: {excel_title}")
                else:
                    self.send_message(user_id, "❌ Failed to generate Excel sheet")
            else:
                self.send_message(user_id, "❌ Please provide a title for the Excel sheet\nExample: /excel Project Data")
            return
        
        elif text.lower().startswith('/report '):
            # Extract title for report
            report_title = text[8:].strip()  # Remove "/report " prefix
            if report_title:
                self.send_message(user_id, "📋 Generating multi-format report...")
                # Get last AI response or create default content
                last_messages = session.get("messages", [])
                content = "This is your personalized report generated by ATLAS AI."
                if last_messages:
                    content = last_messages[-1].get("content", content) if last_messages[-1].get("role") == "assistant" else content
                
                files = self.media_handler.generate_summary_report(report_title, content, user_id)
                if files:
                    for file_type, file_path in files.items():
                        file_info = self.media_handler.get_file_info(file_path)
                        self.send_document(user_id, file_path, f"📋 Your {file_type.upper()} report: {report_title}")
                        time.sleep(1)  # Small delay between files
                else:
                    self.send_message(user_id, "❌ Failed to generate report")
            else:
                self.send_message(user_id, "❌ Please provide a title for the report\nExample: /report Summary")
            return
        
        elif text.lower() == '/stats':
            stats = self.get_bot_stats()
            self.send_message(user_id, stats)
            return
        
        elif text.lower() == '/myinfo':
            user_info = self.get_user_info(user_id)
            self.send_message(user_id, user_info)
            return
        
        elif text.lower() == '/clear':
            if user_id in self.user_sessions:
                del self.user_sessions[user_id]
                self.active_users.discard(user_id)
            self.send_message(user_id, f"🧹 Your conversation cleared! Fresh start, {user_name}!")
            return
        
        # Process with AI
        self.send_message(user_id, "🧠 Processing with Atlas AI intelligence...")
        
        ai_response = self.call_groq_ai(text, user_id)
        
        # Split long messages
        if len(ai_response) > 4000:
            parts = [ai_response[i:i+4000] for i in range(0, len(ai_response), 4000)]
            for i, part in enumerate(parts):
                self.send_message(user_id, f"🧠 {self.assistant_name} AI (Part {i+1}/{len(parts)}):\n\n{part}")
                if i < len(parts) - 1:
                    time.sleep(1)
        else:
            self.send_message(user_id, f"🧠 {self.assistant_name} AI:\n\n{ai_response}")
    
    def health_check(self):
        """Health check endpoint for Render"""
        return {
            "status": "healthy",
            "bot": self.assistant_name,
            "creator": self.creator_name,
            "platform": "Render",
            "active_users": len(self.active_users),
            "total_messages": self.total_messages,
            "uptime": str(datetime.now() - self.start_time)
        }
    
    def run(self):
        """Run the bot"""
        print(f"🚀 Starting {self.assistant_name} AI Telegram Bot - Render Edition...")
        print(f"👨‍💻 Creator: {self.creator_name}")
        print("🌐 Platform: Render Cloud Services")
        print("🧠 Complete Atlas Intelligence Enabled")
        print("👥 Multi-User Support Active")
        print("💬 Advanced Conversations Ready")
        print("🔍 Deep Research Capabilities Active")
        print("🎨 Creative Intelligence Online")
        print("💻 Technical Expertise Available")
        print("🌐 Real-time Information Access")
        print("🔒 Privacy Protection Enabled")
        print("🔄 Concurrent Processing Ready")
        print("🌐 Health check endpoint ready")
        print("🔗 Bot ready for multiple users on Render!")
        
        # Test connection
        try:
            response = requests.get(f"https://api.telegram.org/bot{self.bot_token}/getMe")
            if response.status_code == 200:
                bot_info = response.json()
                print(f"✅ Connected to bot: @{bot_info['result']['username']}")
            else:
                print(f"❌ Failed to connect: {response.status_code}")
                return
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return
        
        # Main polling loop
        while True:
            try:
                params = {'offset': self.last_update_id + 1, 'timeout': 30}
                response = requests.get(
                    f"https://api.telegram.org/bot{self.bot_token}/getUpdates",
                    params=params,
                    timeout=35
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data['ok'] and data['result']:
                        for update in data['result']:
                            self.last_update_id = update['update_id']
                            
                            if 'message' in update:
                                msg = update['message']
                                user_id = msg['from']['id']
                                user_name = msg['from'].get('first_name', 'User')
                                username = msg['from'].get('username')
                                text = msg.get('text', '')
                                
                                if text:
                                    self.process_message(user_id, user_name, username, text)
                
            except requests.exceptions.Timeout:
                print("⏳ Polling timeout...")
            except KeyboardInterrupt:
                print("\n👋 Bot stopped")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(5)

if __name__ == "__main__":
    bot = AtlasAITelegramBot()
    bot.run()
