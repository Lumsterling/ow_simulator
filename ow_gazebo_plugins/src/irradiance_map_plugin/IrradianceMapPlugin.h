/*******************************************************************************
 * Copyright (c) 2018 United States Government as represented by the 
 * Administrator of the National Aeronautics and Space Administration. 
 * All rights reserved.
 ******************************************************************************/
#ifndef IRRADIANCE_MAP_PLUGIN_H
#define IRRADIANCE_MAP_PLUGIN_H

#include <gazebo/common/Plugin.hh>
#include <gazebo/common/common.hh>
#include "CubemapFilter.h"
#include <ros/ros.h>
#include <std_msgs/String.h>
#include <OGRE/OgreCamera.h>
#include <OGRE/OgreTexture.h>

namespace gazebo {

class IrradianceMapPlugin : public VisualPlugin
{
public:
  IrradianceMapPlugin();
  ~IrradianceMapPlugin();

  virtual void Load(rendering::VisualPtr visual, sdf::ElementPtr element);

  bool initialize();

  void onUpdate();

private:
  common::Timer m_timer;

  // Connection to the update event
  event::ConnectionPtr mUpdateConnection;

  Ogre::TexturePtr m_texture;

  // Cameras and viewports for capturing the scene
  Ogre::Camera* m_cameras[6];
  Ogre::Viewport* m_viewports[6];

  // The visual's material. But we want to apply the irradiance map to many scene materials. How to do this?
  Ogre::MaterialPtr m_material;

  std::unique_ptr<CubemapFilter> m_cubemap_filter;
};

}

#endif // IRRADIANCE_MAP_PLUGIN_H
