import { useState } from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { Paperclip, Send, CuboidIcon as Cube } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Toaster } from "@/components/ui/sonner"
import Loader from "react-js-loader";
import { toast } from "sonner"
export default function Home() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  // Function to send query to backend
  const handleSendQuery = async () => {
   
    if (file) {
      // Upload file if attached
      const formData = new FormData();
      formData.append("file", file);

      try {
        setLoading(true);
        const res = await fetch("http://127.0.0.1:8001/upload", {
          method: "POST",
          body: formData,
        });
        setLoading(false);
        const data = await res.json();
        setResponse(`File uploaded: ${data.filename}, Type: ${data.content_type}`);
        setQuery("")
        setFile(null)
        toast("File Upload Sucessfully")
      } catch (error) {
        setLoading(false);
        setQuery("")
        setFile(null)
        console.error("Error uploading file:", error);
        setResponse("Failed to upload file");
        toast("Failed to upload file")

      }
    } else if (query.trim()) {
      // Send query if no file is attached
      console.log("qu")
      try {
        setLoading(true);
        const res = await fetch("http://127.0.0.1:8001/send", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ query }),
        });

        const data = await res.json();
        console.log(data)
        if(data.result.result=="download_file"){
          console.log("getting in...............................")
          fetch('http://localhost:8001/download')
          .then(response => {
              const contentDisposition = response.headers.get('Content-Disposition');
              let filename = 'downloaded_file'; // Default name
      
              if (contentDisposition) {
                  const match = contentDisposition.match(/filename="(.+)"/);
                  if (match && match[1]) {
                      filename = match[1];
                  }
              }
      
              return response.blob().then(blob => ({ blob, filename }));
          })
          .then(({ blob, filename }) => {
              const url = window.URL.createObjectURL(blob);
              const a = document.createElement('a');
              a.href = url;
              a.download = filename; // Use the filename from the backend
              document.body.appendChild(a);
              a.click();
              window.URL.revokeObjectURL(url);
              document.body.removeChild(a);
          })
          .catch(error => console.error('Error downloading file:', error));
        }
        setQuery("")
        setLoading(false);
        toast(data.result.result)
      } catch (error) {
        console.error("Error sending request:", error);
        setResponse("Failed to fetch response");
        setLoading(false);
        toast("Failed to fetch response")
      }
    }
  };

  // Function to handle file selection
  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  return (
    <Router>
      <div className="min-h-screen flex flex-col">
      <header className="border-b border-border">
          <div className="container mx-auto px-4 py-3 flex items-center justify-between">
            <div className="flex items-center gap-8">
              <Link to="/" className="flex items-center gap-2">
                <Cube className="h-6 w-6 text-primary" />
                <span className="font-bold text-xl">DriveGen</span>
              </Link>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <span className="text-sm">Manu</span>
              </div>

    <Dialog>
      <DialogTrigger asChild>
      <Avatar>
      <AvatarImage src="https://github.com/shadcn.png" alt="@shadcn" />
      <AvatarFallback>CN</AvatarFallback>
    </Avatar>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>config profile</DialogTitle>
          <DialogDescription>
            Make changes to your profile here. Click save when you're done.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="name" className="text-right">
              Telegram
            </Label>
            <Input id="name" value="1198847980" className="col-span-3" />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="username" className="text-right">
              Email
            </Label>
            <Input id="username" value="manuzmanuz79@gmail.com" className="col-span-3" />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="username" className="text-right">
              Name
            </Label>
            <Input id="username" value="Manu" className="col-span-3" />
          </div>
        </div>
        <DialogFooter>
          <Button type="submit">Save changes</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

            </div>
          </div>
        </header>

        <main className="flex-1 flex flex-col items-center justify-center px-4 py-12 md:py-24">
          <div className="max-w-3xl w-full space-y-6 text-center">
            <h1 className="text-4xl md:text-5xl font-bold tracking-tight">I Can Help You Manage Files Easily</h1>
            <p className="text-xl text-muted-foreground">Send Drive Files With Natural Language</p>

            <div className="mt-12 space-y-4 w-full">
              <div className="flex items-center border border-border rounded-lg p-3 gap-2">
                <Textarea
                  placeholder="Mention your file name and method to send"
                  className="flex-1 resize-none h-23 border-none focus:ring-0 focus:outline-none"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                />
                
                <input type="file" id="file-upload" className="hidden" onChange={handleFileChange} />
                <Button variant="ghost" size="icon" onClick={() => document.getElementById("file-upload").click()}>
                  <Paperclip className="h-5 w-5" />
                </Button>
                
                <Button className="bg-primary text-primary-foreground hover:bg-primary/90" onClick={handleSendQuery}>
                  <Send className="h-5 w-5" />
                </Button>
              </div>
              
              {/* Display selected file name */}
              {file && (
                <div className="text-sm text-muted-foreground mt-2">
                  <strong>Selected File:</strong> {file.name}
                </div>
              )}
              
              {/* Display the response */}
              {/*response && (
                <div className="text-sm text-muted-foreground mt-4">
                  <strong>Response:</strong> {response}
                </div>
              )*/}
                {loading && (
                  <div className="flex flex-col items-center justify-center h-full w-full text-sm text-muted-foreground mt-4">
                    <Loader type="spinner-circle" bgColor="#000000" color="#000000" title="Agent is thinking..." size={70} />
                  </div>
                )}

            </div>
          </div>
        </main>
        <Toaster/>
      </div>
    </Router>
  );
}