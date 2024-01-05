import { useState } from "react";
import { Routes, Route } from "react-router-dom";
import Topbar from "./scenes/global/Topbar";
import Sidebar from "./scenes/global/Sidebar";
import Dashboard from "./scenes/dashboard";
import Team from "./scenes/team";
import Invoices from "./scenes/invoices";
import Contacts from "./scenes/contacts";
import Bar from "./scenes/bar";
import Form from "./scenes/form";
import Line from "./scenes/line";
import Pie from "./scenes/pie";
import FAQ from "./scenes/faq";
import Geography from "./scenes/geography";
import { CssBaseline, ThemeProvider } from "@mui/material";
import { ColorModeContext, useMode } from "./theme";
import Calendar from "./scenes/calendar/calendar";
import Users from "./scenes/users";
import Provinces from "./scenes/province";
import Districts from "./scenes/districts";
import PlaceCategories from "./scenes/placeCategories";
import Places from "./scenes/places";
import LikeSubCategories from "./scenes/likeSubCategories";
import UserRecords from "./scenes/userRecord";
import Tours from "./scenes/tour";
import { Login } from "@mui/icons-material";
import { QueryClient, QueryClientProvider } from "react-query";

function App() {
  const [theme, colorMode] = useMode();
  const [isSidebar, setIsSidebar] = useState(true);
  const client = new QueryClient({
    defaultOptions: {
      queries: {
        refetchOnWindowFocus: false,
      },
    },
  });

  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <div className="app">
          <Sidebar isSidebar={isSidebar} />
          <main className="content">
            <Topbar setIsSidebar={setIsSidebar} />
            <QueryClientProvider client={client}>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/team" element={<Team />} />
                <Route path="/contacts" element={<Contacts />} />
                <Route path="/invoices" element={<Invoices />} />
                <Route path="/form" element={<Form />} />
                <Route path="/bar" element={<Bar />} />
                <Route path="/pie" element={<Pie />} />
                <Route path="/line" element={<Line />} />
                <Route path="/faq" element={<FAQ />} />
                <Route path="/calendar" element={<Calendar />} />
                <Route path="/geography" element={<Geography />} />
                <Route path="/users" element={<Users />} />
                <Route path="/provinces" element={<Provinces />} />
                <Route path="/districts" element={<Districts />} />
                <Route path="/placeCategories" element={<PlaceCategories />} />
                <Route path="/places" element={<Places />} />
                <Route path="/likeSubCategories" element={<LikeSubCategories />} />
                <Route path="/userRecords" element={<UserRecords />} />
                <Route path="/tours" element={<Tours />} />
                <Route path="/login" element={<Login />} />
              </Routes>
            </QueryClientProvider>
          </main>
        </div>
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
}

export default App;
