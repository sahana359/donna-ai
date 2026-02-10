//
//  ChatView.swift
//  ui
//
//  Created by Sahana Rajashekara on 2/9/26.
//
import SwiftUI

struct ChatView: View {
    @State private var messages: [Message] = []
    @State private var inputText: String = ""
    @State private var isLoading: Bool = false
    
    var body: some View {
        VStack(spacing: 0) {
            ScrollViewReader { proxy in
                ScrollView {
                    LazyVStack(spacing: 12) {
                        ForEach(messages) { message in
                            MessageBubble(message: message)
                                .id(message.id)
                        }
                        
                        if isLoading {
                            ThinkingBubble()
                                .id("thinking")
                        }
                    }
                    .padding()
                    .frame(maxWidth: .infinity)
                }
                .defaultScrollAnchor(.bottom)
                .onChange(of: messages.count) {
                    scrollToBottom(proxy: proxy)
                }
                .onChange(of: isLoading) {
                    if isLoading {
                        withAnimation {
                            proxy.scrollTo("thinking", anchor: .bottom)
                        }
                    }
                }
            }
            
            MessageInputBar(text: $inputText, onSend: sendMessage)
        }
    }
    
    private func sendMessage() {
        let userMessage = Message(content: inputText, isFromUser: true)
        messages.append(userMessage)
        let textToSend = inputText
        inputText = ""
        
        Task {
            await sendToBackend(text: textToSend)
        }
    }
    
    private func scrollToBottom(proxy: ScrollViewProxy) {
        guard let lastMessage = messages.last else { return }
        withAnimation(.easeOut(duration: 0.3)) {
            proxy.scrollTo(lastMessage.id, anchor: .bottom)
        }
    }
    
    private func sendToBackend(text: String) async {
        isLoading = true
        let service = ChatService(baseURL: "http://127.0.0.1:8000")
        
        do {
            let reply = try await service.send(message: text)
            
            await MainActor.run {
                isLoading = false
                let botMessage = Message(content: reply, isFromUser: false)
                messages.append(botMessage)
            }
        } catch {
            print("API error: \(error)")
            await MainActor.run {
                isLoading = false
            }
        }
    }
}
#Preview {
    ChatView()
}
