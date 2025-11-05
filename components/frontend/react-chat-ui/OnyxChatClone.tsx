import React, { useMemo, useState } from 'react';
import {
  MessageCircle,
  Search,
  Palette,
  ChevronDown,
  Plus,
  Send,
  Paperclip,
  Loader2,
} from 'lucide-react';

type AssistantName = 'General' | 'Search' | 'Art';

type ChatMessage = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  assistant: AssistantName;
};

type Assistant = {
  name: AssistantName;
  icon: React.ComponentType<{ size?: number }>;
  description: string;
  placeholder: string;
};

type Suggestion = {
  label: string;
  prompt: string;
  assistant?: AssistantName;
};

const assistants: Assistant[] = [
  {
    name: 'General',
    icon: MessageCircle,
    description:
      'Assistant with no search functionalities. Chat directly with the Large Language Model.',
    placeholder: 'Ask anything or generate content instantly...'
  },
  {
    name: 'Search',
    icon: Search,
    description: 'Search the web and get answers with citations and sources.',
    placeholder: 'Search the web or request recent information...'
  },
  {
    name: 'Art',
    icon: Palette,
    description: 'Generate and edit images with natural language prompts.',
    placeholder: 'Describe the artwork you want to see...'
  }
];

const previousChats = [
  'Hide Mac Dock Shortcut',
  'Login Debug Help',
  'Git Cherry Pick Cmd',
  'Onyx Overview'
];

const baseSuggestions: Suggestion[] = [
  {
    label: 'Summarize a document',
    prompt: 'Summarize the main points from this transcript and highlight action items.',
  },
  {
    label: 'Help me with coding',
    prompt: 'Review this TypeScript utility and point out potential runtime errors.',
  },
  {
    label: 'Draft a professional email',
    prompt: 'Draft a professional follow-up email after a successful product demo.',
  },
  {
    label: 'Learn something new',
    prompt: 'Teach me the difference between optimistic and pessimistic locking with examples.',
  }
];

const getAssistantByName = (name: AssistantName) =>
  assistants.find((assistant) => assistant.name === name) ?? assistants[0];

const getAssistantReply = (assistant: Assistant, userMessage: string) => {
  switch (assistant.name) {
    case 'Search':
      return `I would search trusted sources for “${userMessage}” and deliver a cited summary.`;
    case 'Art':
      return `Rendering an image prompt based on: ${userMessage}. I will generate variations you can refine.`;
    default:
      return `Here is a thoughtful response to “${userMessage}”. Customize this template with project specifics.`;
  }
};

const createMessage = (
  role: ChatMessage['role'],
  content: string,
  assistant: AssistantName
): ChatMessage => ({
  id: `${role}-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
  role,
  content,
  assistant,
});

export default function OnyxChatClone() {
  const [selectedAssistant, setSelectedAssistant] = useState<AssistantName>('General');
  const [message, setMessage] = useState('');
  const [showPreviousChats, setShowPreviousChats] = useState(true);
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [isGeneratingReply, setIsGeneratingReply] = useState(false);

  const assistant = useMemo(
    () => getAssistantByName(selectedAssistant),
    [selectedAssistant]
  );

  const suggestions = useMemo<Suggestion[]>(() =>
    baseSuggestions.map((suggestion) => ({
      ...suggestion,
      assistant: suggestion.assistant ?? selectedAssistant,
    })),
  [selectedAssistant]);

  const handleSendMessage = (input?: string) => {
    const content = (input ?? message).trim();

    if (!content || isGeneratingReply) {
      return;
    }

    const userMessage = createMessage('user', content, selectedAssistant);
    setChatHistory((history) => [...history, userMessage]);
    setMessage('');
    setIsGeneratingReply(true);

    // Simulate assistant response so the UI feels alive even without a backend.
    setTimeout(() => {
      setChatHistory((history) => [
        ...history,
        createMessage('assistant', getAssistantReply(assistant, content), selectedAssistant),
      ]);
      setIsGeneratingReply(false);
    }, 650);
  };

  const handleSuggestionClick = (suggestion: Suggestion) => {
    setSelectedAssistant(suggestion.assistant ?? selectedAssistant);
    setMessage(suggestion.prompt);
    handleSendMessage(suggestion.prompt);
  };

  const handleKeyDown: React.KeyboardEventHandler<HTMLTextAreaElement> = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex h-screen bg-[#f5f5f5] text-gray-900">
      {/* Sidebar */}
      <div className="w-80 bg-black flex flex-col">
        {/* Logo */}
        <div className="p-4">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center">
              <span className="text-black font-bold">O</span>
            </div>
            <span className="text-xl font-semibold text-white">onyx</span>
          </div>
        </div>

        {/* New Chat Button */}
        <button className="mx-4 mt-2 px-4 py-3 bg-[#1e2936] hover:bg-[#2a3744] text-white rounded-lg flex items-center gap-2 transition-colors">
          <Plus size={18} />
          <span>New Chat</span>
        </button>

        {/* Assistants */}
        <div className="mt-6 px-4">
          <h3 className="text-xs font-semibold text-gray-500 uppercase mb-3 tracking-wider">Assistants</h3>
          <div className="space-y-1">
            {assistants.map((assistant) => (
              <button
                key={assistant.name}
                onClick={() => setSelectedAssistant(assistant.name)}
                className={`w-full px-4 py-3 rounded-lg flex items-center gap-3 transition-colors ${
                  selectedAssistant === assistant.name
                    ? 'bg-[#2a3744] text-white'
                    : 'text-gray-400 hover:bg-[#1a1a1a] hover:text-white'
                }`}
              >
                <assistant.icon size={20} />
                <span>{assistant.name}</span>
              </button>
            ))}
          </div>
          <button className="mt-3 px-4 text-sm text-gray-500 hover:text-gray-400 transition-colors">
            Explore Assistants
          </button>
        </div>

        {/* Previous Chats */}
        <div className="mt-6 px-4 flex-1 overflow-y-auto">
          <button
            onClick={() => setShowPreviousChats(!showPreviousChats)}
            className="flex items-center gap-2 text-xs font-semibold text-gray-500 uppercase mb-3 hover:text-gray-400 tracking-wider"
          >
            <ChevronDown
              size={14}
              className={`transition-transform ${showPreviousChats ? '' : '-rotate-90'}`}
            />
            <span>Chats</span>
          </button>
          {showPreviousChats && (
            <>
              <div className="text-xs text-gray-600 mb-2 px-4">Previous 7 Days</div>
              <div className="space-y-0.5">
                {previousChats.map((chat, idx) => (
                  <button
                    key={idx}
                    className="w-full px-4 py-2 text-sm text-left text-gray-400 hover:text-white transition-colors"
                  >
                    {chat}
                  </button>
                ))}
              </div>
            </>
          )}
        </div>

        {/* User Profile */}
        <div className="p-4">
          <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
            <span className="text-white font-semibold">Y</span>
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col bg-white">
        {/* Header */}
        <div className="border-b border-gray-200 p-8">
          <div className="flex items-center gap-3 mb-2">
            <assistant.icon size={32} className="text-gray-400" />
            <h1 className="text-3xl font-normal text-gray-300">{selectedAssistant}</h1>
          </div>
          <p className="text-gray-400">{assistant.description}</p>
        </div>

        {/* Chat Content */}
        <div className="flex-1 p-8 overflow-y-auto">
          <div className="max-w-3xl mx-auto space-y-4">
            {chatHistory.length === 0 && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {suggestions.map((suggestion) => (
                  <button
                    key={suggestion.label}
                    onClick={() => handleSuggestionClick(suggestion)}
                    className="p-6 bg-[#1e2a38] hover:bg-[#253445] text-white rounded-2xl text-left transition-colors"
                  >
                    <span className="block text-sm uppercase tracking-wide text-gray-400 mb-2">
                      {suggestion.assistant ?? selectedAssistant}
                    </span>
                    <span className="font-medium text-base leading-relaxed">
                      {suggestion.prompt}
                    </span>
                  </button>
                ))}
              </div>
            )}

            {chatHistory.map((entry) => (
              <div
                key={entry.id}
                className={`rounded-2xl px-5 py-4 text-sm leading-relaxed shadow-sm border ${
                  entry.role === 'user'
                    ? 'bg-white border-gray-200 text-gray-800'
                    : 'bg-[#101621] border-[#1f2c3a] text-gray-100'
                }`}
              >
                <div className="flex items-center gap-2 text-xs uppercase tracking-wide mb-2">
                  <span className="text-gray-400">{entry.role === 'user' ? 'You' : entry.assistant}</span>
                </div>
                <p>{entry.content}</p>
              </div>
            ))}

            {isGeneratingReply && (
              <div className="rounded-2xl px-5 py-4 bg-[#101621] border border-[#1f2c3a] text-gray-200 flex items-center gap-3">
                <Loader2 className="animate-spin" size={18} />
                <span>Thinking…</span>
              </div>
            )}
          </div>
        </div>

        {/* Input Area */}
        <div className="p-8">
          <div className="max-w-4xl mx-auto">
            <div className="bg-[#1e2a38] rounded-2xl overflow-hidden">
              <textarea
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder={assistant.placeholder}
                className="w-full bg-transparent px-6 py-4 text-white placeholder-gray-500 resize-none focus:outline-none"
                rows={1}
              />
              <div className="flex items-center justify-between px-6 py-3 border-t border-gray-700">
                <div className="flex items-center gap-4">
                  <button className="flex items-center gap-2 text-sm text-gray-400 hover:text-gray-300 transition-colors">
                    <Paperclip size={18} />
                    <span>File</span>
                  </button>
                  <button className="flex items-center gap-2 text-sm text-gray-400 hover:text-gray-300 transition-colors">
                    <span>Claude 3.5 Sonnet (New)</span>
                    <ChevronDown size={14} />
                  </button>
                </div>
                <button
                  onClick={() => handleSendMessage()}
                  disabled={isGeneratingReply || !message.trim()}
                  className="text-gray-400 hover:text-white transition-colors disabled:text-gray-600 disabled:cursor-not-allowed"
                >
                  <Send size={20} />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
