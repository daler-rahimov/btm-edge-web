import GettingStarted from "views/GettingStarted/GettingStarted";
import ShotControls from "views/ShotControls/ShotControls";
import WirelessConnection from "views/WirelessConnection/WirelessConnection";

// @material-ui/icons
import PlayCircleFilledIcon from "@material-ui/icons/PlayCircleFilled";
import SportsEsportsIcon from "@material-ui/icons/SportsEsports";
import SettingsInputAntennaIcon from "@material-ui/icons/SettingsInputAntenna";

var dashRoutes = [
  {
    path: "/getting-started",
    name: "Getting Started",
    rtlName: "",
    icon: PlayCircleFilledIcon,
    component: GettingStarted,
    layout: "/admin",
  },
  {
    path: "/shot-controls",
    name: "Shot Controls",
    rtlName: "",
    icon: SportsEsportsIcon,
    component: ShotControls,
    layout: "/admin",
  },
  {
    path: "/wireless-connection",
    name: "Wireless Connection",
    rtlName: "",
    icon: SettingsInputAntennaIcon,
    component: WirelessConnection,
    layout: "/admin",
  },
];
export default dashRoutes;
